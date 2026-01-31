# app/config.py
from pydantic import BaseModel
import os

"""
配置项统一集中管理，支持从环境变量加载。
"""

class Settings(BaseModel):
    # 数据库连接（POC 用 SQLite 或 PostgreSQL 均可）
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./backend/data/exai_poc.db")

    # H2O 相关配置
    H2O_URL: str = os.getenv("H2O_URL", "http://localhost:54321")

    # MLflow 相关配置
    MLFLOW_TRACKING_URI: str = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")

    # 服务基础配置
    API_PREFIX: str = "/api"
    API_V1_PREFIX: str = "/api/v1"

    # 多租户默认租户
    DEFAULT_TENANT_ID: str = os.getenv("DEFAULT_TENANT_ID", "default_tenant")


settings = Settings()
