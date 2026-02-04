# app/api/v1/registry_api.py
from fastapi import APIRouter
from app.schemas.registry_schemas import RegisterModelRequest, ModelRegistryEntrySchema
from app.adapters.mlflow_adapter import MLflowAdapter
from app.domain.model_govern.service import ModelGovernService
from app.infra.db import SessionLocal
from app.infra.repositories.service_repo import ServiceRepository

router = APIRouter(prefix="/registry", tags=["registry"])


@router.post("/register", response_model=ModelRegistryEntrySchema)
def register_model(req: RegisterModelRequest):
    """
    模型注册接口：
    - 直接调用 ModelGovernService.register_model
    """
    mlflow_client = MLflowAdapter()
    db = SessionLocal()
    try:
        service_repo = ServiceRepository(db)
        svc = ModelGovernService(mlflow_client, service_repo)
        reg = svc.register_model(req.name, req.artifact_uri, req.description or "")
        return ModelRegistryEntrySchema(**reg.model_dump())
    finally:
        db.close()
