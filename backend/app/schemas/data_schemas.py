# app/schemas/data_schemas.py
from pydantic import BaseModel
from typing import Any, Dict, List, Optional

"""
数据源
"""
class DataSourceSchema(BaseModel):
    id: str
    name: str
    type: str
    config: Dict

class DataSourceCreateSchema(BaseModel):
    name: str
    type: str
    config: Dict

class DataSourceUpdateSchema(BaseModel):
    name: str
    type: str
    config: Dict

"""
数据集
"""
class DatasetSchema(BaseModel):
    id: str
    name: str
    source_id: str
    table_name: str
    description: Optional[str]

class DatasetCreateSchema(BaseModel):
    name: str
    source_id: str
    table_name: str
    description: Optional[str]

class DatasetUpdateSchema(BaseModel):
    name: str
    source_id: str
    table_name: str
    description: Optional[str]

"""
数据集预览
"""
class DatasetPreviewSchema(BaseModel):
    columns: List[str]
    rows: List[Dict[Any, Any]]
