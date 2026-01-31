# app/adapters/mlflow_adapter.py
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import mlflow
from mlflow.tracking import MlflowClient
from mlflow.h2o import log_model
from app.config import settings

"""
MLflow 适配器：封装 Tracking + Model Registry 能力。
"""

class MLflowClientAdapter(ABC):
    @abstractmethod
    def start_run(self, experiment_name: str, run_name: Optional[str] = None) -> str:
        ...

    @abstractmethod
    def log_params(self, run_id: str, params: Dict[str, Any]) -> None:
        ...

    @abstractmethod
    def log_metrics(self, run_id: str, metrics: Dict[str, float]) -> None:
        ...

    @abstractmethod
    def log_model(self, run_id: str, model, artifact_path: str) -> str:
        ...

    @abstractmethod
    def register_model(self, model_uri: str, name: str) -> str:
        ...

    @abstractmethod
    def transition_model_stage(self, name: str, version: str, stage: str) -> None:
        ...

    @abstractmethod
    def get_model_version(self, name: str, version: str) -> Dict[str, Any]:
        ...


class MLflowSdkAdapter(MLflowClientAdapter):
    def __init__(self):
        mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)

    def _get_mlflow_client(self):
        mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
        return MlflowClient()
    
    def _get_or_create_experiment(self, experiment_name: str) -> str:
        exp = mlflow.get_experiment_by_name(experiment_name)
        if exp is None:
            exp_id = mlflow.create_experiment(experiment_name)
        else:
            exp_id = exp.experiment_id
        return exp_id

    def start_run(self, experiment_name: str, run_name: Optional[str] = None) -> str:
        exp_id = self._get_or_create_experiment(experiment_name)
        run = mlflow.start_run(experiment_id=exp_id, run_name=run_name)
        return run.info.run_id

    def log_params(self, run_id: str, params: Dict[str, Any]) -> None:
        with mlflow.start_run(run_id=run_id):
            mlflow.log_params(params)

    def log_metrics(self, run_id: str, metrics: Dict[str, float]) -> None:
        with mlflow.start_run(run_id=run_id):
            mlflow.log_metrics(metrics)

    def log_model(self, run_id: str, model, artifact_path: str) -> str:
        with mlflow.start_run(run_id=run_id):
            log_model(model, artifact_path=artifact_path)
            # 模型 URI 形如：runs:/<run_id>/<artifact_path>
            return f"runs:/{run_id}/{artifact_path}"

    def register_model(self, model_uri: str, name: str) -> str:
        result = mlflow.register_model(model_uri=model_uri, name=name)
        return result.version

    def transition_model_stage(self, name: str, version: str, stage: str) -> None:
        client = mlflow.MlflowClient()
        client.transition_model_version_stage(
            name=name,
            version=version,
            stage=stage,
        )

    def get_model_version(self, name: str, version: str) -> Dict[str, Any]:
        client = mlflow.MlflowClient()
        mv = client.get_model_version(name=name, version=version)
        return {
            "name": mv.name,
            "version": mv.version,
            "current_stage": mv.current_stage,
            "source": mv.source,
        }



