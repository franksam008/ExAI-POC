# app/domain/model_govern/models.py
from typing import Any, Dict, Optional
from pydantic import BaseModel
from enum import Enum
from app.constants import SERVICE_STATUS_RUNNING, SERVICE_STATUS_STOPPED


class ModelStage(str, Enum):
    STAGING = "Staging"
    PRODUCTION = "Production"
    ARCHIVED = "Archived"


class ServiceStatus(str, Enum):
    RUNNING = SERVICE_STATUS_RUNNING
    STOPPED = SERVICE_STATUS_STOPPED


class ModelRegistryEntry(BaseModel):
    """
    模型注册信息，映射到 MLflow Model Registry。
    """
    name: str
    version: int
    stage: ModelStage
    description: Optional[str] = None
    mlflow_model_uri: str


class ModelService(BaseModel):
    """
    模型服务信息，记录服务配置与状态。
    """
    id: str
    name: str
    model_name: str
    model_version: int
    endpoint: str
    status: ServiceStatus
    config: Dict[str, Any] = {}
