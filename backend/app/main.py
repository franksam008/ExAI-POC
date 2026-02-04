# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.logging import setup_logging
from app.api.v1 import (
    auth_api,
    data_api,
    workflow_api,
    workflow_template_api,
    registry_api, 
    deploy_api, 
    monitor_api, 
    system_api, 
)
from app.infra.db import Base, engine

setup_logging()
app = FastAPI(title="ExAI POC")

# 重要：启动时创建所有 ORM 表，保证 POC 可运行
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_api.router, prefix="/api/v1") 
app.include_router(data_api.router, prefix="/api/v1") 
app.include_router(workflow_api.router, prefix="/api/v1")
app.include_router(workflow_template_api.router, prefix="/api/v1")
app.include_router(registry_api.router, prefix="/api/v1") 
app.include_router(deploy_api.router, prefix="/api/v1") 
app.include_router(monitor_api.router, prefix="/api/v1") 
app.include_router(system_api.router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "ok"}
