# app/api/v1/monitor_api.py
from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime, timedelta
import random

router = APIRouter(prefix="/monitor", tags=["monitor"])


class MetricPoint(BaseModel):
    timestamp: str
    qps: float
    latency_ms: float
    error_rate: float


@router.get("/services/{service_id}/metrics", response_model=list[MetricPoint])
def get_service_metrics(service_id: str):
    """
    服务监控数据：
    - POC：返回一段时间内的随机曲线数据，方便前端画图
    """
    now = datetime.utcnow()
    points = []
    for i in range(20):
        t = now - timedelta(minutes=20 - i)
        points.append(
            MetricPoint(
                timestamp=t.isoformat(),
                qps=random.uniform(10, 100),
                latency_ms=random.uniform(50, 300),
                error_rate=random.uniform(0, 0.1),
            )
        )
    return points


from fastapi import APIRouter
from app.adapters.mlflow_adapter import MLflowSdkAdapter

@router.get("/models/{name}/{version}")
def get_model_metrics(name: str, version: str):
    """
    从 MLflow 中获取某个模型版本的指标
    """
    client = MLflowSdkAdapter()
    mlflow_client = client._get_mlflow_client()
    mv = mlflow_client.get_model_version(name=name, version=version)
    if mv and mv.run_id:
        run = mlflow_client.get_run(mv.run_id)
        return {
        "name": name,
        "version": version,
        "metrics": run.data.metrics,
        "params": run.data.params,
        }
    else:
        return {}
