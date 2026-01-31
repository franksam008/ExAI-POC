# app/infra/repositories/user_repo.py
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.infra.db import Base
from app.infra.repositories.base_repo import BaseRepository

"""
用户 ORM 与仓储：
- POC：只做展示，不做真正认证
"""

class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class UserRepository(BaseRepository):
    def list_all(self):
        return (
            self.db.query(UserORM)
            .filter(UserORM.tenant_id == self.tenant_id)
            .order_by(UserORM.created_at.desc())
            .all()
        )
