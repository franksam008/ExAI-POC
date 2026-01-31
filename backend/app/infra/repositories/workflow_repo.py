# app/infra/repositories/workflow_repo.py
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from app.infra.db import Base
from app.infra.repositories.base_repo import BaseRepository

"""
工作流相关 ORM 与仓储：
- POC：只存 workflow 定义 JSON，不存节点拆分表
"""

class WorkflowORM(Base):
    __tablename__ = "workflows"

    id = Column(String(36), primary_key=True, index=True)
    tenant_id = Column(String(64), index=True)
    name = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    definition_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class WorkflowRepository(BaseRepository):
    """
    工作流仓储：
    - 负责保存与读取工作流定义
    """

    def save(self, wf_id: str, tenant_id: str, name: str, description: str, definition_json: str) -> None:
        obj = WorkflowORM(
            id=wf_id,
            tenant_id=tenant_id,
            name=name,
            description=description,
            definition_json=definition_json,
        )
        self.db.add(obj)
        self.db.commit()

    def get(self, wf_id: str, tenant_id: str) -> Optional[WorkflowORM]:
        return (
            self.db.query(WorkflowORM)
            .filter(WorkflowORM.id == wf_id, WorkflowORM.tenant_id == tenant_id)
            .first()
        )
