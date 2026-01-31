# app/schemas/data_schemas.py
from pydantic import BaseModel
from typing import Any, Dict, List

class DataSourceSchema(BaseModel):
    id: str
    name: str
    type: str


class DatasetSchema(BaseModel):
    id: str
    name: str


class DatasetPreviewSchema(BaseModel):
    columns: List[str]
    rows: List[Dict[Any, Any]]
