# backend/app/adapters/h2o_adapter.py
import requests
from typing import Any, Dict, List
from app.config import settings
import json

class H2OHttpAdapter:
    def __init__(self):
        self.base = settings.H2O_BASE_URL.rstrip("/")

    # ---------- 通用 ----------
    def _wait_job(self, job_id: str):
        while True:
            r = requests.get(f"{self.base}/3/Jobs/{job_id}")
            r.raise_for_status()
            job = r.json()["jobs"][0]
            if job["status"] == "DONE":
                return
            if job["status"] == "FAILED":
                raise RuntimeError(f"H2O job failed: {job_id}")

    def _get_model_from_job(self, job_id: str) -> str:
        r = requests.get(f"{self.base}/3/Jobs/{job_id}")
        r.raise_for_status()
        return r.json()["jobs"][0]["dest"]["name"]

    # ---------- 数据 / Frame ----------
    def import_file(self, path: str) -> str:
        r = requests.post(f"{self.base}/3/ImportFiles", data={"path": path})
        r.raise_for_status()
        return r.json()["destination_frames"][0]

    def list_frames(self) -> List[str]:
        r = requests.get(f"{self.base}/3/Frames")
        r.raise_for_status()
        return [item["frame_id"]["name"] for item in r.json()["frames"]]
    
    def parse_setup(self, source_frames: List[str]) -> Dict[str, Any]:
        r = requests.post(f"{self.base}/3/ParseSetup", data={"source_frames": source_frames})
        r.raise_for_status()
        return r.json()
    
    def parse(self, destination_frame: str, parse_setup: Dict[str, Any]) -> Dict[str, Any]:        
        all_parse_setup = {
            "destination_frame": destination_frame,
            "source_frames": [item["name"] for item in parse_setup["source_frames"]],
            "parse_type": parse_setup["parse_type"],
            "separator": parse_setup["separator"],
            "single_quotes": parse_setup["single_quotes"],
            "check_header": parse_setup["check_header"],
            "number_columns": parse_setup["number_columns"],
            "column_names": parse_setup["column_names"],
            "column_types": parse_setup["column_types"],
            #"domain": null,
            "force_col_types": parse_setup["force_col_types"],
            "na_strings": parse_setup["na_strings"],
            "chunk_size": parse_setup["chunk_size"],
            "delete_on_done": False,
            "blocking": True,
            "decrypt_tool": parse_setup["decrypt_tool"],
            "custom_non_data_line_markers": parse_setup["custom_non_data_line_markers"],
            "partition_by": parse_setup["partition_by"],
            "tz_adjust_to_local": parse_setup["tz_adjust_to_local"],
            "_exclude_fields": parse_setup["_exclude_fields"],
            "skipped_columns": parse_setup["skipped_columns"],
            "escapechar": parse_setup["escapechar"],
        }
        #print(f"parse setup: {json.dumps(all_parse_setup)}")
        r = requests.post(f"{self.base}/3/Parse", data=all_parse_setup)
        r.raise_for_status()
        return {
            "source_frames": r.json()["source_frames"][0]["name"], 
            "destination_frame": r.json()["destination_frame"]["name"]
            }

    def split_frame(self, dataset: str, ratios: List[float], destination_frames: List[str], seed: int = 1234) -> List[str]:
        r = requests.post(f"{self.base}/3/SplitFrame", 
                          data={"dataset": dataset, 
                                "ratios": ratios, 
                                "destination_frames": destination_frames})
        r.raise_for_status()
        return [item["name"] for item in r.json()["destination_frames"]]
    
    # ---------- 预处理 / 特征工程 ----------
    def standardize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        # params 至少包含 training_frame
        r = requests.post(f"{self.base}/3/ModelBuilders/standardize", data=params)
        r.raise_for_status()
        job_id = r.json()["job"]["key"]["name"]
        self._wait_job(job_id)
        return {"job_id": job_id, "training_frame": params["training_frame"]}

    def pca(self, params: Dict[str, Any]) -> Dict[str, Any]:
        r = requests.post(f"{self.base}/3/ModelBuilders/pca", data=params)
        r.raise_for_status()
        job_id = r.json()["job"]["key"]["name"]
        self._wait_job(job_id)
        return {"job_id": job_id, "training_frame": params["training_frame"]}

    # ---------- 训练（统一入口，支持 GBM/DRF/GLM/XGBoost/AutoML 等） ----------
    def train(self, algo: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        params 至少包含: training_frame, response_column
        其他超参直接透传
        """
        print(f"开始训练：{algo}")
        print(f"训练参数: {json.dumps(params)}")

        """
        payload = {
            "model_id": "iris_gbm_v1",
            "training_frame": "iris_train",
            "validation_frame": "iris_test",
            "response_column": "variety",
            "ntrees": 20,
            "max_depth": 5,
            "learn_rate": 0.1,
            "seed": 1234
        }     

        print(f"硬编码训练参数: {json.dumps(payload)}")
        """

        r = requests.post(
            f"{self.base}/3/ModelBuilders/{algo}",
            data=params,                     # ← 必须解析成k1=v1&k2=v2...的形式，不能使用json
            headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}  # ← 必须指定，不能使用application/json（通过h2o webui的post访问得出）
        )

        print(f"训练任务提交结果: \n {json.dumps(r.json())}")
        r.raise_for_status()        
        job_id = r.json()["job"]["key"]["name"]
        print(f"训练任务id: \n {job_id}")
        #self._wait_job(job_id)
        model_id = self._get_model_from_job(job_id)
        return {"job_id": job_id, "model_id": model_id}

    # ---------- 评估 ----------
    def evaluate(self, model_id: str, frame_id: str) -> Dict[str, Any]:
        r = requests.post(f"{self.base}/3/ModelMetrics/models/{model_id}/frames/{frame_id}")
        print(f"评估路径：{self.base}/3/ModelMetrics/models/{model_id}/frames/{frame_id}")
        r.raise_for_status()
        metrics = r.json()["model_metrics"][0]
        #return r.json()
        return {"metrics": metrics}

    # ---------- 预测 ----------
    def predict(self, model_id: str, frame_id: str) -> Dict[str, Any]:
        r = requests.post(f"{self.base}/3/Predictions/models/{model_id}/frames/{frame_id}")
        r.raise_for_status()
        pred_frame = r.json()["predictions_frame"]["name"]
        return {"predictions_frame": pred_frame}

    # ---------- 模型导出 ----------
    def export_model(self, export_type: str, model_id: str, export_path: str) -> Dict[str, Any]:
        params = {
            "dir" : export_path,
            "force": True
        }
        if export_type == "bin":
            url_path = f"{self.base}/99/Models.bin/{model_id}"
        else:
            url_path = f"{self.base}/99/Models.mojo/{model_id}"

        r = requests.get(url_path, params=params)
        r.raise_for_status()

        return {"model_id": model_id, "model_path": r.json()["dir"]}
