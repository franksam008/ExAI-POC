# app/dependencies.py
from sqlalchemy.orm import Session
from fastapi import Depends
from app.infra.db import SessionLocal
from app.constants import DEFAULT_TENANT_ID

"""
全局依赖封装：
- DB Session
- 当前租户 / 当前用户（POC：固定）
"""

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_tenant_id() -> str:
    # POC：固定一个租户，后续可从 JWT 中解析
    return DEFAULT_TENANT_ID


def get_current_user_id() -> str:
    # POC：固定一个用户 ID
    return "demo-user"
