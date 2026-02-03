from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional, List
from app.infra.db import Base
from app.infra.repositories.base_repo import BaseRepository


class DataSourceORM(Base):
    __tablename__ = "data_sources"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    type: Mapped[str] = mapped_column(String(32), nullable=False)  # local_db / mysql / postgres / s3 / http
    config_json: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class DataSourceRepository(BaseRepository):
    def list_all(self) -> List[DataSourceORM]:
        return (
            self.db.query(DataSourceORM)
            .filter(DataSourceORM.tenant_id == self.tenant_id)
            .order_by(DataSourceORM.created_at.desc())
            .all()
        )

    def get(self, datasource_id: str) -> Optional[DataSourceORM]:
        return (
            self.db.query(DataSourceORM)
            .filter(
                DataSourceORM.tenant_id == self.tenant_id,
                DataSourceORM.id == datasource_id,
            )
            .first()
        )

    def save(self, row: DataSourceORM):
        self.db.add(row)
        self.db.commit()

    def delete(self, ds_id: str):
        row = self.get(ds_id)
        if row:
            self.db.delete(row)
            self.db.commit()
