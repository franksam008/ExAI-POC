# app/api/v1/data_api.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
from app.dependencies import get_db, get_current_tenant_id
from app.infra.repositories.datasource_repo import DataSourceRepository, DataSourceORM
from app.infra.repositories.dataset_repo import DatasetRepository, DatasetORM
from app.schemas.data_schemas import (
    DataSourceSchema, 
    DataSourceCreateSchema, 
    DataSourceUpdateSchema,
    DatasetSchema, 
    DatasetCreateSchema, 
    DatasetUpdateSchema, 
    DatasetPreviewSchema)
import json
from uuid import uuid4

router = APIRouter(prefix="/data", tags=["data"])

# -------------------------
# 数据源 CRUD
# -------------------------
@router.get("/sources", response_model=list[DataSourceSchema])
def list_data_sources(db: Session = Depends(get_db),
                  tenant_id: str = Depends(get_current_tenant_id)):
    """
    数据源列表：
    """
    repo = DataSourceRepository(db, tenant_id)
    ds = repo.list_all()

    return [DataSourceSchema(
        id=d.id, 
        name=d.name, 
        type=d.type, 
        config=json.loads(d.config_json if d.config_json else "{}")) 
        for d in ds]

@router.post("/sources", response_model=str)
def create_source(payload: DataSourceCreateSchema, 
                  db: Session = Depends(get_db), 
                  tenant_id: str = Depends(get_current_tenant_id)): 
    repo = DataSourceRepository(db, tenant_id) 
    row = DataSourceORM( 
        id=str(uuid4()), 
        tenant_id=tenant_id, 
        name=payload.name, 
        type=payload.type, 
        config_json=json.dumps(payload.config), 
    ) 
    repo.save(row) 
    return row.id

@router.put("/sources/{source_id}")
def update_source(source_id: str, 
                  payload: DataSourceUpdateSchema, 
                  db: Session = Depends(get_db), 
                  tenant_id: str = Depends(get_current_tenant_id)): 
    repo = DataSourceRepository(db, tenant_id) 
    row = repo.get(source_id)
    if row:
        row.name = payload.name 
        row.type = payload.type 
        row.config_json = json.dumps(payload.config)
        repo.save(row) 
    return {"status": "ok"}

@router.delete("/sources/{source_id}")
def delete_source(source_id: str, 
                  db: Session = Depends(get_db), 
                  tenant_id: str = Depends(get_current_tenant_id)): 
    repo = DataSourceRepository(db, tenant_id) 
    repo.delete(source_id) 
    return {"status": "ok"}

# -------------------------
# 数据集 CRUD
# -------------------------
@router.get("/datasets", response_model=list[DatasetSchema])
def list_all_datasets(db: Session = Depends(get_db), 
                      tenant_id: str = Depends(get_current_tenant_id)):
    repo = DatasetRepository(db, tenant_id)
    rows = repo.list_all()
    return [
        DatasetSchema(
            id=r.id,
            name=r.name,
            source_id=r.source_id,
            table_name=r.table_name,
            description=r.description,
        )
        for r in rows
    ]

@router.get("/sources/{source_id}/datasets", response_model=list[DatasetSchema])
def list_datasets_by_source(source_id: str,
                  db: Session = Depends(get_db),
                  tenant_id: str = Depends(get_current_tenant_id)):
    """
    数据集列表：
    """
    repo = DatasetRepository(db, tenant_id)
    ds = repo.list_by_source(source_id)
    return [
        DatasetSchema(
            id=r.id,
            name=r.name,
            source_id=r.source_id,
            table_name=r.table_name,
            description=r.description,
        )
        for r in ds
    ]


@router.post("/datasets", response_model=str)
def create_dataset(payload: DatasetCreateSchema, db: Session = Depends(get_db), tenant_id: str = Depends(get_current_tenant_id)):
    repo = DatasetRepository(db, tenant_id)
    row = DatasetORM(
        id=str(uuid4()),
        tenant_id=tenant_id,
        name=payload.name,
        source_id=payload.source_id,
        table_name=payload.table_name,
        description=payload.description,
    )
    repo.save(row)
    return row.id


@router.put("/datasets/{dataset_id}")
def update_dataset(dataset_id: str, payload: DatasetUpdateSchema, db: Session = Depends(get_db), tenant_id: str = Depends(get_current_tenant_id)):
    repo = DatasetRepository(db, tenant_id)
    row = repo.get(dataset_id)
    if row:
        row.name = payload.name
        row.source_id = payload.source_id
        row.table_name = payload.table_name
        row.description = payload.description
        repo.save(row)
    return {"status": "ok"}


@router.delete("/datasets/{dataset_id}")
def delete_dataset(dataset_id: str, db: Session = Depends(get_db), tenant_id: str = Depends(get_current_tenant_id)):
    repo = DatasetRepository(db, tenant_id)
    repo.delete(dataset_id)
    return {"status": "ok"}


@router.get("/datasets/{dataset_id}/preview")
def preview_dataset(dataset_id: str, 
                    page: int = 1, 
                    page_size: int = 20,
                    db: Session = Depends(get_db),
                    tenant_id: str = Depends(get_current_tenant_id),
                    ):
    """
    数据集预览：
    """
    repo = DatasetRepository(db, tenant_id)
    ds = repo.get(dataset_id)
    if not ds: 
        raise HTTPException(status_code=404, detail="dataset not found") 
    
    # 这里假设你在同一个 DB 里有对应的物理表 ds.table_name
    offset = (page - 1) * page_size
    sql = f"SELECT * FROM {ds.table_name} LIMIT {page_size} OFFSET {offset}"
    with db.connection() as conn:
        df = pd.read_sql(sql, conn) 

    return DatasetPreviewSchema(
        columns=list(df.columns), 
        rows=df.to_dict(orient="records"),
    )

@router.get("/datasets/{dataset_id}/profile")
def dataset_profile(dataset_id: str,
                    db: Session = Depends(get_db),
                    tenant_id: str = Depends(get_current_tenant_id),
                    ):
    """
    数据探查：
    - 使用 pandas.describe 计算统计特征
    - 只做简单统计，POC 足够
    """
    query = f"SELECT * FROM {dataset_id} LIMIT 10000"
    with db.connection() as conn:
        df = pd.read_sql(query, conn)

    desc = df.describe(include="all").transpose().reset_index()
    return {
        "summary": desc.to_dict(orient="records"),
    }





