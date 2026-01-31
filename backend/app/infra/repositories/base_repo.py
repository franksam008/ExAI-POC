# app/infra/repositories/base_repo.py
from sqlalchemy.orm import Session
from app.constants import DEFAULT_TENANT_ID

"""
所有仓储的基类，统一注入 tenant_id 过滤逻辑。
"""

class BaseRepository:
    def __init__(self, db: Session, tenant_id: str = DEFAULT_TENANT_ID):
        """
        所有仓储的基类：
        - 统一持有 db session 和 tenant_id
        - 约定所有查询都必须带 tenant_id
        """
        self.db = db
        self.tenant_id = tenant_id
