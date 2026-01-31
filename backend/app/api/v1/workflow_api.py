# app/api/v1/workflow_api.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.workflow_schemas import WorkflowCreateSchema, WorkflowRunSchema
from app.domain.workflow.models import WorkflowDefinition
from app.domain.workflow.executor import WorkflowExecutor
from app.domain.model_dev.service import ModelDevService
from app.domain.model_govern.service import ModelGovernService
from app.adapters.h2o_adapter import H2OHttpClient
from app.adapters.mlflow_adapter import MLflowSdkAdapter
from app.infra.db import SessionLocal

router = APIRouter(prefix="/workflows", tags=["workflows"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_executor() -> WorkflowExecutor:
    # 重要：POC 直接在依赖中组装依赖树，生产可用 DI 容器
    h2o_client = H2OHttpClient()
    mlflow_client = MLflowSdkAdapter()
    model_dev_service = ModelDevService(h2o_client, mlflow_client)
    # service_repo 在此略，POC 可用内存或简单 SQLite 实现
    from app.infra.repositories.service_repo import ServiceRepository
    from app.infra.db import SessionLocal

    db = SessionLocal()
    service_repo = ServiceRepository(db)
    model_govern_service = ModelGovernService(mlflow_client, service_repo)
    return WorkflowExecutor(model_dev_service, model_govern_service)


@router.post("", response_model=str)
def create_workflow(wf: WorkflowCreateSchema, db: Session = Depends(get_db)):
    """
    创建工作流定义。
    POC：直接将 JSON 存入数据库（略），返回一个 UUID。
    """
    from uuid import uuid4

    wf_id = str(uuid4())
    # TODO: 写入 workflows 表，这里略实现，重点在执行链路
    return wf_id


@router.post("/{workflow_id}/run", response_model=WorkflowRunSchema)
def run_workflow(workflow_id: str, wf: WorkflowCreateSchema, executor: WorkflowExecutor = Depends(get_executor)):
    """
    执行工作流：
    - 为了 POC 简化，前端直接把完整 WorkflowDefinition 传过来，不从 DB 读取。
    """
    wf_def = WorkflowDefinition(
        id=workflow_id,
        name=wf.name,
        description=wf.description,
        nodes=[n.to_domain() for n in wf.nodes],
    )
    run = executor.execute(wf_def)
    return WorkflowRunSchema.from_domain(run)
