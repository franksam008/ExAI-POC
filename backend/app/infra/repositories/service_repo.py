# app/infra/repositories/service_repo.py
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.orm import Session, Mapped, mapped_column
from datetime import datetime
from typing import Optional, List
import json
from app.infra.db import Base
from app.infra.repositories.base_repo import BaseRepository
from app.domain.model_govern.models import ModelService, ServiceStatus
from app.constants import DEFAULT_TENANT_ID

"""
模型服务 ORM 与仓储：
- 记录服务配置，用于推理时查找对应模型
"""

class ModelServiceORM(Base):
    __tablename__ = "model_services"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    model_name: Mapped[str] = mapped_column(String(128), nullable=False)
    model_version: Mapped[str] = mapped_column(String(32), nullable=False)
    endpoint: Mapped[str] = mapped_column(String(256), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    config_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ServiceRepository(BaseRepository):
    """
    模型服务仓储：
    - 保存服务信息
    - 根据 service_id 查询服务
    """

    def save(self, service: ModelService) -> None:
        existing = (
            self.db.query(ModelServiceORM) 
            .filter(
                ModelServiceORM.tenant_id == self.tenant_id, 
                ModelServiceORM.id == service.id, ) 
            .first()
            )
        if existing:
            existing.name = service.name
            existing.model_name = service.model_name
            existing.model_version = str(service.model_version)
            existing.endpoint = service.endpoint
            existing.status = service.status.value
            existing.config_json = json.dumps(service.config)
        else:
            obj = ModelServiceORM(
                id=service.id,
                tenant_id=self.tenant_id,
                name=service.name,
                model_name=service.model_name,
                model_version=str(service.model_version),
                endpoint=service.endpoint,
                status=service.status.value,
                config_json=json.dumps(service.config),
            )
            self.db.add(obj)
        self.db.commit()

    def get(self, service_id: str) -> Optional[ModelService]:
        obj = (
            self.db.query(ModelServiceORM)
            .filter(ModelServiceORM.id == service_id, ModelServiceORM.tenant_id == self.tenant_id)
            .first()
        )
        if not obj:
            return None
        return ModelService(
            id=obj.id,
            name=obj.name,
            model_name=obj.model_name,
            model_version=int(obj.model_version),
            endpoint=obj.endpoint,
            status=ServiceStatus(obj.status),
            config=json.loads(obj.config_json or "{}"),
        )

    def list_all(self) -> List[ModelService]:
        objs = (
            self.db.query(ModelServiceORM)
            .filter(ModelServiceORM.tenant_id == self.tenant_id)
            .order_by(ModelServiceORM.created_at.desc())
            .all()
        )
        return [
            ModelService(
                id=o.id,
                name=o.name,
                model_name=o.model_name,
                model_version=int(o.model_version),
                endpoint=o.endpoint,
                status=ServiceStatus(o.status),
                config=json.loads(o.config_json or "{}"),
            )
            for o in objs
        ]
