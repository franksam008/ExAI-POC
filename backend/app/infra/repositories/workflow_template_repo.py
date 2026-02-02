from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import List, Optional
from app.infra.db import Base
from app.infra.repositories.base_repo import BaseRepository

class WorkflowTemplateORM(Base):
    __tablename__ = "workflow_templates"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(String(64), nullable=True)  # classification/regression/automl
    definition_json: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class WorkflowTemplateRepository(BaseRepository):
    def list_template(self, category: Optional[str] = None) -> List[WorkflowTemplateORM]:
        q = self.db.query(WorkflowTemplateORM).filter(
            WorkflowTemplateORM.tenant_id == self.tenant_id            
        )
        if category:
            q = q.filter(WorkflowTemplateORM.category == category)
        return q.order_by(WorkflowTemplateORM.created_at.desc()).all()
        

    def get_by_id(self, template_id: str) -> Optional[WorkflowTemplateORM]:
        return (
            self.db.query(WorkflowTemplateORM)
            .filter(
                WorkflowTemplateORM.tenant_id == self.tenant_id,
                WorkflowTemplateORM.id == template_id,
            )
            .first()
        )

    def get_by_name(self, name: str) -> Optional[WorkflowTemplateORM]:
        return (
            self.db.query(WorkflowTemplateORM)
            .filter(
                WorkflowTemplateORM.tenant_id == self.tenant_id,
                WorkflowTemplateORM.name == name,
            )
            .first()
        )

    def save(self, tpl: WorkflowTemplateORM):
        self.db.add(tpl)
        self.db.commit()

    def delete(self, category_id: str):
        row = self.get_by_id(category_id)
        if row:
            self.db.delete(row)
            self.db.commit()
