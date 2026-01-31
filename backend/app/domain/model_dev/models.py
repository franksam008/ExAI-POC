# app/domain/model_dev/models.py
from typing import Any, Dict, List
from pydantic import BaseModel
from enum import Enum
from app.constants import ALGO_H2O_GBM


class AlgorithmType(str, Enum):
    H2O_GBM = ALGO_H2O_GBM


class TrainRequest(BaseModel):
    """
    训练请求模型，封装训练所需的关键参数。
    """
    dataset_ref: str  # 数据集引用（例如表名或 SQL）
    target_column: str
    feature_columns: List[str]
    algorithm: AlgorithmType
    params: Dict[str, Any]
    experiment_name: str


class TrainResult(BaseModel):
    """
    训练结果模型，包含模型 ID、指标、工件路径等。
    """
    model_id: str
    metrics: Dict[str, float]
    artifact_uri: str
    mlflow_run_id: str
