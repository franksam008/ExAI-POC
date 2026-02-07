# backend/app/adapters/mlflow_adapter.py
import mlflow
import h2o
from mlflow.entities.model_registry import ModelVersion
from typing import Dict, Any, List
from app.config import settings
from datetime import datetime

class MLflowAdapter:
    def __init__(self):
        mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)        
        self.client = mlflow.MlflowClient()

    # ---------- 日志记录 ----------
    def log_model_artifact(
        self,
        model_path: str,
        params: Dict[str, Any] | None = None,
        metrics: Dict[str, Any] | None = None,
        tags: Dict[str, Any] | None = None,
    ) -> str:
        with mlflow.start_run():
            if params:
                mlflow.log_params(params)
            if metrics:
                mlflow.log_metrics(metrics)
            if tags:
                mlflow.set_tags(tags)
            mlflow.log_artifact(model_path, artifact_path="model")
            active_run = mlflow.active_run()
            if active_run:
                run_id = active_run.info.run_id
            else:
                run_id = "not running model"
        return run_id

    # ---------- 模型注册 ----------
    def load_h2o_model(self, model_name: str, model_path: str) -> Dict[str,Any]:
        h2o.connect(url=settings.H2O_BASE_URL)
        h2o_model = h2o.import_mojo(model_path)
        experiment_name = "iris_gbm_experiment"
        mlflow.set_experiment(experiment_name)
        with mlflow.start_run(run_name=f"{model_name}-run-{datetime.now()}"):
            model_info = mlflow.h2o.log_model(
                h2o_model = h2o_model,
                name = model_name,
                registered_model_name = model_name,
            )
        return {
            "run_id": model_info.run_id,
            "name": model_info.name,
            "model_id": model_info.model_id,
            "model_uri": model_info.model_uri,             
            "registered_model_version": model_info.registered_model_version,
        }

    # ---------- 模型注册 ----------
    def register_model(self, run_id: str, model_name: str) -> str:
        model_uri = f"runs:/{run_id}/model"
        result = mlflow.register_model(model_uri, model_name)
        return result.name

    # ---------- 阶段切换 ----------
    def transition_stage(self, model_name: str, version: int, stage: str):
        self.client.transition_model_version_stage(
            name=model_name,
            version=str(version),
            stage=stage,
        )

    # ---------- 获取模型列表 ----------
    def list_models(self) -> List[Dict[str, Any]]:
        models = self.client.search_registered_models()
        result = []
        for m in models:
            mlv: ModelVersion = m.latest_versions[0]
            result.append({
                "name": mlv.name,
                "version": mlv.version,
                "current_stage": "NA",
                "description": mlv.description,
                "last_updated_timestamp": mlv.last_updated_timestamp,
            })
        return result
        return [{
            "name": m.name,
            "version": m.latest_versions,
            "current_stage": "NA",
            "description": m.description,
            "last_updated_timestamp": m.last_updated_timestamp,
        } for m in models]

    # ---------- 获取模型版本 ----------
    def list_model_versions(self, model_name: str | None = None) -> List[Dict[str, Any]]: #List[ModelVersion]:
        filter_str = f"name='{model_name}'" if model_name else None
        versions = self.client.search_model_versions(filter_str)

        #return versions
        # TODO: 自定义ModelVersion模型，兼容mlflow的ModelVersion模型，但不绑定其模型
        
        return [{
                 "run_id": v.run_id,
                 "name": v.name,
                 "model_id": v.model_id,
                 "version": v.version,
                 "current_stage": v.current_stage,
                 "last_updated_timestamp": v.last_updated_timestamp,
                 "description": v.description,
                 "metrics": v.metrics,
                 "params": v.params,
                 "tags": v._tags,
                 } for v in versions]
        
        

    # ---------- 获取 run 参数 / 指标 ----------
    def get_run_params_metrics(self, run_id: str) -> Dict[str, Any]:
        run = self.client.get_run(run_id)
        return {
            "params": run.data.params,
            "metrics": run.data.metrics,
            "tags": run.data.tags,
        }

    # ---------- 启停“服务”（这里抽象为：标记某个版本为 Production / Archived 等） ----------
    def set_model_stage(self, model_name: str, version: int, stage: str):
        # 实际上就是 transition_stage 的语义封装
        self.transition_stage(model_name, version, stage)
