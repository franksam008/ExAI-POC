from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db, get_current_tenant_id
from app.domain.workflow.template_service import WorkflowTemplateService
from app.schemas.workflow_template_schemas import WorkflowTemplateSchema, WorkflowTemplateCreateSchema
from app.dependencies import get_workflow_template_service

router = APIRouter(prefix="/workflow-templates", tags=["workflow-templates"])

@router.get("", response_model=List[WorkflowTemplateSchema])
def list_templates(svc: WorkflowTemplateService = Depends(get_workflow_template_service)):
    return svc.list_templates()


@router.get("/{template_id}", response_model=WorkflowTemplateSchema)
def get_template(template_id: str, 
                 svc: WorkflowTemplateService = Depends(get_workflow_template_service)):
    return svc.get_template(template_id)


@router.post("", response_model=str)
def create_template(tpl: WorkflowTemplateCreateSchema, 
                    svc: WorkflowTemplateService = Depends(get_workflow_template_service)):
    return svc.create_template(tpl)
