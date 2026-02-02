from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.dependencies import get_db, get_current_tenant_id
from app.domain.workflow.template_service import WorkflowTemplateService
from app.schemas.workflow_template_schemas import WorkflowTemplateSchema, WorkflowTemplateCreateSchema
from app.dependencies import get_workflow_template_service

router = APIRouter(prefix="/workflow-templates", tags=["workflow-templates"])

# GET /workflow-templates?category=xxx
@router.get("", response_model=List[WorkflowTemplateSchema])
def list_templates(category: Optional[str] = None,
                   svc: WorkflowTemplateService = Depends(get_workflow_template_service)):
    return svc.list_templates(category)


@router.get("/{template_id}", response_model=WorkflowTemplateSchema)
def get_template(template_id: str, 
                 svc: WorkflowTemplateService = Depends(get_workflow_template_service)):
    return svc.get_template_by_id(template_id)


@router.post("", response_model=str)
def create_template(tpl: WorkflowTemplateCreateSchema, 
                    svc: WorkflowTemplateService = Depends(get_workflow_template_service)):
    return svc.create_template(tpl)
