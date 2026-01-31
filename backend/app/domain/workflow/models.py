# app/domain/workflow/models.py
from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel
from app.constants import (
    NODE_TYPE_DATA_SOURCE,
    NODE_TYPE_PREPROCESS,
    NODE_TYPE_FEATURE_ENGINEERING,
    NODE_TYPE_DATASET_PROCESS,
    NODE_TYPE_TRAIN,
    NODE_TYPE_EVALUATE,
    NODE_TYPE_REGISTER,
    NODE_TYPE_DEPLOY,
)


class NodeType(str, Enum):
    DATA_SOURCE = NODE_TYPE_DATA_SOURCE
    PREPROCESS = NODE_TYPE_PREPROCESS
    FEATURE_ENGINEERING = NODE_TYPE_FEATURE_ENGINEERING
    DATASET_PROCESS = NODE_TYPE_DATASET_PROCESS
    TRAIN = NODE_TYPE_TRAIN
    EVALUATE = NODE_TYPE_EVALUATE
    REGISTER = NODE_TYPE_REGISTER
    DEPLOY = NODE_TYPE_DEPLOY


class WorkflowNode(BaseModel):
    """
    工作流节点模型，对应前端画布中的一个节点。
    """
    id: str
    type: NodeType
    name: str
    params: Dict[str, Any] = {}
    upstream_ids: List[str] = []


class WorkflowDefinition(BaseModel):
    """
    工作流定义模型，包含节点列表。
    """
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    version: int = 1
    nodes: List[WorkflowNode]


class RunStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


class WorkflowRun(BaseModel):
    """
    工作流运行实例，用于记录执行状态。
    """
    id: str
    workflow_id: str
    status: RunStatus
    started_at: datetime
    finished_at: Optional[datetime] = None
    context: Dict[str, Any] = {}
