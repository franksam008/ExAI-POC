# app/infra/repositories/dataset_repo.py
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import List, Optional
from app.infra.db import Base
from app.infra.repositories.base_repo import BaseRepository

class DatasetORM(Base):
    """
    数据集元数据表：
    - POC：把可用的数据表/视图登记在这里
    """
    __tablename__ = "datasets"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    source_id: Mapped[str] = mapped_column(String(64), index=True)  # 如 local_db
    name: Mapped[str] = mapped_column(String(128), nullable=False)  # 展示名称
    table_name: Mapped[str] = mapped_column(String(128), nullable=False)  # 实际 DB 表名
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class DatasetRepository(BaseRepository):
    def list_by_source(self, source_id: str) -> List[DatasetORM]:
        return (
            self.db.query(DatasetORM)
            .filter(
                DatasetORM.tenant_id == self.tenant_id,
                DatasetORM.source_id == source_id,
            )
            .order_by(DatasetORM.created_at.desc())
            .all()
        )

    def get(self, dataset_id: str) -> Optional[DatasetORM]:
        return (
            self.db.query(DatasetORM)
            .filter(
                DatasetORM.tenant_id == self.tenant_id,
                DatasetORM.id == dataset_id,
            )
            .first()
        )
