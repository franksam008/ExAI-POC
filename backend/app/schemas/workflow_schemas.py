# app/schemas/workflow_schemas.py
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from app.domain.workflow.models import WorkflowNode, WorkflowDefinition, RunStatus, NodeType, WorkflowRun


class WorkflowNodeSchema(BaseModel):
    id: str
    type: NodeType
    name: str
    params: Dict[str, Any] = {}
    upstream_ids: List[str] = []

    def to_domain(self) -> WorkflowNode:
        return WorkflowNode(
            id=self.id,
            type=self.type,
            name=self.name,
            params=self.params,
            upstream_ids=self.upstream_ids,
        )


class WorkflowCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None
    nodes: List[WorkflowNodeSchema]


class WorkflowRunSchema(BaseModel):
    id: str
    workflow_id: str
    status: RunStatus
    context: Dict[str, Any]

    @classmethod
    def from_domain(cls, run: WorkflowRun):
        return cls(
            id=run.id,
            workflow_id=run.workflow_id,
            status=run.status,
            context=run.context,
        )
