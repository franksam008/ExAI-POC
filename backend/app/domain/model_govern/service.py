# app/domain/model_govern/service.py
from typing import Dict, Any
from uuid import uuid4
from app.domain.model_govern.models import (
    ModelRegistryEntry,
    ModelStage,
    ModelService,
    ServiceStatus,
)
from app.adapters.mlflow_adapter import MLflowAdapter
from app.infra.repositories.service_repo import ServiceRepository

"""
模型治理服务：
- 注册模型到 MLflow Model Registry
- 在本 FastAPI 内部注册一个推理服务（POC：单机、简单路由）
"""

class ModelGovernService:
    def __init__(self, mlflow_client: MLflowAdapter, service_repo: ServiceRepository):
        self.mlflow_client = mlflow_client
        self.service_repo = service_repo

    def register_model(self, name: str, artifact_uri: str, description: str = "") -> ModelRegistryEntry:
        version = self.mlflow_client.register_model(artifact_uri, name)
        # 默认阶段设为 Staging
        self.mlflow_client.transition_stage(name, int(version), ModelStage.STAGING.value)
        return ModelRegistryEntry(
            name=name,
            version=int(version),
            stage=ModelStage.STAGING,
            description=description,
            mlflow_model_uri=artifact_uri,
        )

    def deploy_model(self, name: str, version: int, config: Dict[str, Any]) -> ModelService:
        service_id = str(uuid4())
        endpoint = f"/api/v1/services/predict/{service_id}"

        # 重要：确保 config 中包含模型 URI，供推理使用
        # 如果上游 context 中有 mlflow_model_uri，可在调用时传入
        if "model_uri" not in config and "mlflow_model_uri" in config:
            config["model_uri"] = config["mlflow_model_uri"]

        service = ModelService(
            id=service_id,
            name=f"{name}_v{version}",
            model_name=name,
            model_version=version,
            endpoint=endpoint,
            status=ServiceStatus.RUNNING,
            config=config,
        )
        self.service_repo.save(service)
        return service
