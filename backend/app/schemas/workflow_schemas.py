# backend/app/schemas/workflow_schemas.py
from pydantic import BaseModel
from typing import Any, Dict, List, Optional

class WorkflowNodePosition(BaseModel):
    x: float
    y: float


class WorkflowNodeSchema(BaseModel):
    id: str
    type: str          # h2o_import / h2o_prep / h2o_train / h2o_eval / h2o_predict / h2o_export / mlflow_log / mlflow_register / mlflow_transition / mlflow_get_run / mlflow_list_versions ...
    label: str
    params: Dict[str, Any]
    position: WorkflowNodePosition


class WorkflowEdgeSchema(BaseModel):
    id: str
    source: str
    target: str


class WorkflowDAGSchema(BaseModel):
    nodes: List[WorkflowNodeSchema]
    edges: List[WorkflowEdgeSchema]


class WorkflowSchema(BaseModel):
    id: str
    name: str
    description: Optional[str]
    dag: WorkflowDAGSchema


class WorkflowCreateSchema(BaseModel):
    name: str
    description: Optional[str]
    dag: WorkflowDAGSchema


class WorkflowUpdateSchema(BaseModel):
    name: str
    description: Optional[str]
    dag: WorkflowDAGSchema
