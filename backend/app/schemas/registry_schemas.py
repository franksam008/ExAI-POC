# app/schemas/registry_schemas.py
from pydantic import BaseModel
from typing import Optional
from app.domain.model_govern.models import ModelStage

class RegisterModelRequest(BaseModel):
    name: str
    artifact_uri: str
    description: Optional[str] = None


class ModelRegistryEntrySchema(BaseModel):
    name: str
    version: int
    stage: ModelStage
    description: Optional[str] = None
    mlflow_model_uri: str
