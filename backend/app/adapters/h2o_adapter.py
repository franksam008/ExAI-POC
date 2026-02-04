# backend/app/adapters/h2o_adapter.py
import requests
from typing import Any, Dict, List
from app.config import settings


class H2OAdapter:
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
        return r.json()["destination_frames"][0]["name"]

    def list_frames(self) -> List[Dict[str, Any]]:
        r = requests.get(f"{self.base}/3/Frames")
        r.raise_for_status()
        return r.json()["frames"]

    # ---------- 预处理 / 特征工程 ----------
    def standardize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        # params 至少包含 training_frame
        r = requests.post(f"{self.base}/3/ModelBuilders/standardize", json=params)
        r.raise_for_status()
        job_id = r.json()["job"]["key"]["name"]
        self._wait_job(job_id)
        return {"job_id": job_id, "training_frame": params["training_frame"]}

    def pca(self, params: Dict[str, Any]) -> Dict[str, Any]:
        r = requests.post(f"{self.base}/3/ModelBuilders/pca", json=params)
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
        r = requests.post(f"{self.base}/3/ModelBuilders/{algo}", json=params)
        r.raise_for_status()
        job_id = r.json()["job"]["key"]["name"]
        self._wait_job(job_id)
        model_id = self._get_model_from_job(job_id)
        return {"job_id": job_id, "model_id": model_id}

    # ---------- 评估 ----------
    def evaluate(self, model_id: str, frame_id: str) -> Dict[str, Any]:
        r = requests.get(f"{self.base}/3/Models/{model_id}/frames/{frame_id}")
        r.raise_for_status()
        metrics = r.json()["model_metrics"][0]
        return {"metrics": metrics}

    # ---------- 预测 ----------
    def predict(self, model_id: str, frame_id: str) -> Dict[str, Any]:
        r = requests.post(f"{self.base}/3/Predictions/models/{model_id}/frames/{frame_id}")
        r.raise_for_status()
        pred_frame = r.json()["predictions_frame"]["name"]
        return {"predictions_frame": pred_frame}

    # ---------- 模型导出 ----------
    def download_model(self, model_id: str, path: str) -> Dict[str, Any]:
        r = requests.get(f"{self.base}/3/Models/{model_id}/download")
        r.raise_for_status()
        with open(path, "wb") as f:
            f.write(r.content)
        return {"model_path": path}
