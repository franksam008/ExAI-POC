# app/infra/repositories/audit_repo.py
from sqlalchemy import Column, String, DateTime, BigInteger, Text
from datetime import datetime
import json
from app.infra.db import Base
from app.infra.repositories.base_repo import BaseRepository

"""
审计日志 ORM 与仓储：
- 记录简单操作行为
"""

class AuditLogORM(Base):
    __tablename__ = "audit_logs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    tenant_id = Column(String(64), index=True)
    user_id = Column(String(36))
    action = Column(String(128))
    detail_json = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class AuditRepository(BaseRepository):
    def add_log(self, user_id: str, action: str, detail: dict):
        obj = AuditLogORM(
            tenant_id=self.tenant_id,
            user_id=user_id,
            action=action,
            detail_json=json.dumps(detail, ensure_ascii=False),
        )
        self.db.add(obj)
        self.db.commit()

    def list_recent(self, limit: int = 50):
        return (
            self.db.query(AuditLogORM)
            .filter(AuditLogORM.tenant_id == self.tenant_id)
            .order_by(AuditLogORM.created_at.desc())
            .limit(limit)
            .all()
        )
