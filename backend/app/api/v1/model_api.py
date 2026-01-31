# app/api/v1/model_api.py
from fastapi import APIRouter
from app.schemas.model_schemas import TrainRequestSchema, TrainResultSchema
from app.adapters.h2o_adapter import H2OHttpClient
from app.adapters.mlflow_adapter import MLflowSdkAdapter
from app.domain.model_dev.service import ModelDevService

router = APIRouter(prefix="/models", tags=["models"])


@router.post("/train", response_model=TrainResultSchema)
def train_model(req: TrainRequestSchema):
    """
    直接训练接口（非工作流场景）：
    - 方便快速验证训练链路
    """
    h2o_client = H2OHttpClient()
    mlflow_client = MLflowSdkAdapter()
    svc = ModelDevService(h2o_client, mlflow_client)

    temp_req = req.to_domain()
    result = svc.train(temp_req)
    return TrainResultSchema(**result.model_dump())

# app/api/v1/model_api.py
from fastapi import APIRouter
from app.adapters.mlflow_adapter import MLflowSdkAdapter

router = APIRouter(prefix="/models", tags=["models"])

@router.get("")
def list_models():
    """
    返回 MLflow Model Registry 中的所有模型及版本
    """
    client = MLflowSdkAdapter()
    mlflow_client = client._get_mlflow_client()

    models = mlflow_client.search_registered_models()

    result = []
    for m in models:
        if m.latest_versions:
            for v in m.latest_versions:
                result.append({
                    "name": m.name,
                    "version": v.version,
                    "stage": v.current_stage,
                    "source": v.source,
                    "description": m.description,
                })
    return result
