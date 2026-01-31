# app/api/v1/deploy_api.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import mlflow
import pandas as pd
from app.infra.db import SessionLocal
from app.infra.repositories.service_repo import ServiceRepository
from app.dependencies import get_db, get_current_tenant_id
from app.config import Settings

router = APIRouter(prefix="/services", tags=["deploy"])

class ServiceListItem(BaseModel):
    id: str
    name: str
    model_name: str
    model_version: int
    endpoint: str
    status: str


class PredictRequest(BaseModel):
    """
    推理请求：
    - POC：直接传入一条记录的特征字典
    """
    features: dict


@router.get("", response_model=list[ServiceListItem])
def list_services(db: Session = Depends(get_db), tenant_id: str = Depends(get_current_tenant_id)):
    repo = ServiceRepository(db, tenant_id=tenant_id)
    services = repo.list_all()
    return [
        ServiceListItem(
            id=s.id,
            name=s.name,
            model_name=s.model_name,
            model_version=s.model_version,
            endpoint=s.endpoint,
            status=s.status.value,
        )
        for s in services
    ]


@router.post("/predict/{service_id}")
def predict(service_id: str, req: PredictRequest, db: Session = Depends(get_db),
            tenant_id: str = Depends(get_current_tenant_id)):
    """
    推理接口：
    - 根据 service_id 查找模型信息
    - 使用 MLflow 加载模型并进行预测
    """
    repo = ServiceRepository(db, tenant_id=tenant_id)
    service = repo.get(service_id)
    if not service:
        raise HTTPException(status_code=404, detail="service not found")

    # 加载模型：runs:/<run_id>/model 形式
    mlflow.set_tracking_uri(Settings.MLFLOW_TRACKING_URI)
    #mlflow.set_tracking_uri("http://localhost:5000")  # 可改为 settings
    model_uri = service.config.get("model_uri") or service.config.get("mlflow_model_uri")
    if not model_uri:
        # POC：如果 config 中没有，直接用 source 字段（可在部署时写入）
        raise HTTPException(status_code=500, detail="model uri not configured")

    model = mlflow.pyfunc.load_model(model_uri)
    df = pd.DataFrame([req.features])
    preds = model.predict(df)
    # 只返回第一条预测结果
    return {"prediction": preds[0] if len(preds) else None}
