# backend/app/api/v1/model_api.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import List
import json

from app.dependencies import get_db, get_current_tenant_id
from app.adapters.mlflow_adapter import MLflowAdapter
from app.schemas.model_schemas import (
    ModelInfoSchema
)

router = APIRouter(prefix="/models", tags=["models"])

@router.get("", response_model=List[ModelInfoSchema])
def list_models(db: Session = Depends(get_db), 
                tenant_id: str = Depends(get_current_tenant_id)):
    """
    模型注册接口：
    - 直接调用 ModelGovernService.register_model
    """
    mlflow_client = MLflowAdapter()
    mvs = mlflow_client.list_models()
    return [
        ModelInfoSchema(
            name= item["name"], 
            version= str(item["version"]), 
            current_stage= item["current_stage"], 
            description= item["description"],
            last_updated_timestamp= item["last_updated_timestamp"]
        ) for item in mvs
    ]
