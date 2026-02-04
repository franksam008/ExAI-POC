# backend/app/api/v1/workflow_api.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import uuid4
import json

from app.dependencies import get_db, get_current_tenant_id
from app.infra.repositories.workflow_repo import WorkflowRepository, WorkflowORM
from app.schemas.workflow_schemas import (
    WorkflowSchema,
    WorkflowCreateSchema,
    WorkflowUpdateSchema,
    WorkflowDAGSchema,
)
from app.domain.workflow.workflow_executor import WorkflowExecutor

router = APIRouter(prefix="/workflows", tags=["workflows"])


@router.get("", response_model=list[WorkflowSchema])
def list_workflows(db: Session = Depends(get_db), 
                   tenant_id: str = Depends(get_current_tenant_id)):
    repo = WorkflowRepository(db, tenant_id)
    rows = repo.list_all()
    return [
        WorkflowSchema(
            id=r.id,
            name=r.name,
            description=r.description,
            dag=WorkflowDAGSchema(**json.loads(r.definition_json)),
        )
        for r in rows
    ]


@router.post("", response_model=str)
def create_workflow(payload: WorkflowCreateSchema, 
                    db: Session = Depends(get_db), 
                    tenant_id: str = Depends(get_current_tenant_id)):
    repo = WorkflowRepository(db, tenant_id)
    row = WorkflowORM(
        id=str(uuid4()),
        tenant_id=tenant_id,
        name=payload.name,
        description=payload.description,
        definition_json=json.dumps(payload.dag.dict()),
    )
    repo.save(row)
    return row.id


@router.put("/{workflow_id}")
def update_workflow(workflow_id: str, 
                    payload: WorkflowUpdateSchema, 
                    db: Session = Depends(get_db), 
                    tenant_id: str = Depends(get_current_tenant_id)):
    repo = WorkflowRepository(db, tenant_id)
    row = repo.get(workflow_id)
    if row:
        row.name = payload.name
        row.description = payload.description
        row.definition_json = json.dumps(payload.dag.model_dump())
        repo.save(row)
    return {"status": "ok"}


@router.get("/{workflow_id}", response_model=WorkflowSchema)
def get_workflow(workflow_id: str, 
                 db: Session = Depends(get_db), 
                 tenant_id: str = Depends(get_current_tenant_id)):
    repo = WorkflowRepository(db, tenant_id)
    row = repo.get(workflow_id)
    if row:
        wf = WorkflowSchema(
        id=row.id,
        name=row.name,
        description=row.description,
        dag=WorkflowDAGSchema(**json.loads(row.definition_json)),
        )
    else:
        wf = None
    return wf

@router.delete("/{workflow_id}")
def delete_workflow(workflow_id: str, 
                    db: Session = Depends(get_db), 
                    tenant_id: str = Depends(get_current_tenant_id)):
    repo = WorkflowRepository(db, tenant_id)
    repo.delete(workflow_id)
    return {"status": "ok"}


@router.post("/{workflow_id}/run")
def run_workflow(workflow_id: str, 
                 db: Session = Depends(get_db), 
                 tenant_id: str = Depends(get_current_tenant_id)):
    repo = WorkflowRepository(db, tenant_id)
    row = repo.get(workflow_id)
    if row:
        dag = WorkflowDAGSchema(**json.loads(row.definition_json))

        executor = WorkflowExecutor()
        result = executor.execute(dag)
    else:
        result = {}
    return result
