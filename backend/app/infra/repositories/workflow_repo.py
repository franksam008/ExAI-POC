# app/infra/repositories/workflow_repo.py
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.orm import Session, Mapped, mapped_column
from datetime import datetime
from typing import Optional, List
from app.infra.db import Base
from app.infra.repositories.base_repo import BaseRepository

"""
工作流相关 ORM 与仓储：
- POC：只存 workflow 定义 JSON，不存节点拆分表
"""

class WorkflowORM(Base):
    __tablename__ = "workflows"

    id: Mapped[str]= mapped_column(String(36), primary_key=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    definition_json: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class WorkflowRepository(BaseRepository):
    def list_all(self) -> List[WorkflowORM]:
        return (
            self.db.query(WorkflowORM)
            .filter(WorkflowORM.tenant_id == self.tenant_id)
            .order_by(WorkflowORM.created_at.desc())
            .all()
        )

    def get(self, wf_id: str) -> Optional[WorkflowORM]:
        return (
            self.db.query(WorkflowORM)
            .filter(
                WorkflowORM.tenant_id == self.tenant_id,
                WorkflowORM.id == wf_id,
            )
            .first()
        )

    def save(self, row: WorkflowORM):
        self.db.add(row)
        self.db.commit()

    def delete(self, wf_id: str):
        row = self.get(wf_id)
        if row:
            self.db.delete(row)
            self.db.commit()

