# app/schemas/deploy_schemas.py
from pydantic import BaseModel
from typing import Any, Dict

class ServiceCreateRequest(BaseModel):
    model_name: str
    model_version: int
    config: Dict[str, Any] = {}
