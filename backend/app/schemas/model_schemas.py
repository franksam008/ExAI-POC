# app/schemas/model_schemas.py
from pydantic import BaseModel
from typing import Any, Dict, List
from app.domain.model_dev.models import AlgorithmType, TrainRequest

class TrainRequestSchema(BaseModel):
    dataset_ref: str
    target_column: str
    feature_columns: List[str] = []
    algorithm: AlgorithmType = AlgorithmType.H2O_GBM
    params: Dict[str, Any] = {}
    experiment_name: str

    def to_domain(self) -> TrainRequest:
        return TrainRequest(
            dataset_ref=self.dataset_ref,
            target_column=self.target_column,
            feature_columns=self.feature_columns,
            algorithm=self.algorithm,
            params=self.params,
            experiment_name=self.experiment_name
        )

    @classmethod
    def from_domain(cls, req: TrainRequest):
        return cls(
            dataset_ref=req.dataset_ref,
            target_column=req.target_column,
            feature_columns=req.feature_columns,
            algorithm=req.algorithm,
            params=req.params,
            experiment_name=req.experiment_name,
        )


class TrainResultSchema(BaseModel):
    model_id: str
    metrics: Dict[str, float]
    artifact_uri: str
    mlflow_run_id: str
