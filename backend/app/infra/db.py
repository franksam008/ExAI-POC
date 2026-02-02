# app/infra/db.py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

"""
数据库基础设施层，统一创建 SQLAlchemy Engine 和 Session。
"""

engine = create_engine(
    settings.DATABASE_URL,
    echo=False,  # POC 可改为 True 方便调试
    future=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

"""
with engine.connect() as conn:
    result = conn.execute(text("SELECT sqlite_version();"))
    print("SQLite version:", result.scalar())
"""