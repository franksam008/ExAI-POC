from uuid import uuid4
import json
from typing import List, Optional
from app.infra.repositories.workflow_template_repo import WorkflowTemplateRepository, WorkflowTemplateORM
from app.schemas.workflow_template_schemas import WorkflowTemplateCreateSchema, WorkflowTemplateSchema

class WorkflowTemplateService:
    def __init__(self, repo: WorkflowTemplateRepository):
        self.repo = repo

    def list_templates(self, category: Optional[str]) -> List[WorkflowTemplateSchema]:
        rows = self.repo.list_template(category)
        return [
            WorkflowTemplateSchema(
                id=r.id,
                name=r.name,
                description=r.description,
                category=r.category,
                definition=json.loads(r.definition_json),
            )
            for r in rows
        ]

    def get_template_by_id(self, template_id: str) -> WorkflowTemplateSchema | None:
        r = self.repo.get_by_id(template_id)
        if r:
            return WorkflowTemplateSchema(
                id=r.id,
                name=r.name,
                description=r.description,
                category=r.category,
                definition=json.loads(r.definition_json),
            )
        else:
            return None

    def create_template(self, tpl: WorkflowTemplateCreateSchema) -> str:
        tpl_id = str(uuid4())
        row = WorkflowTemplateORM(
            id=tpl_id,
            tenant_id=self.repo.tenant_id,
            name=tpl.name,
            description=tpl.description,
            category=tpl.category,
            definition_json=json.dumps(tpl.definition),
        )
        self.repo.save(row)
        return tpl_id
