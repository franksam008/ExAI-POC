# app/api/v1/data_api.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
from app.dependencies import get_db, get_current_tenant_id
from app.infra.repositories.dataset_repo import DatasetRepository
from app.schemas.data_schemas import DataSourceSchema, DatasetSchema, DatasetPreviewSchema

router = APIRouter(prefix="/data", tags=["data"])

@router.get("/sources", response_model=list[DataSourceSchema])
def list_data_sources():
    """
    数据源列表：
    POC：返回一个固定的“本地数据库”数据源。
    """
    return [
        {
            "id": "local_db",
            "name": "本地数据库",
            "type": "db",
        }
    ]


@router.get("/sources/{source_id}/datasets", response_model=list[DatasetSchema])
def list_datasets(source_id: str,
                  db: Session = Depends(get_db),
                  tenant_id: str = Depends(get_current_tenant_id)):
    """
    数据集列表：
    POC：通过 information_schema 查询所有表。
    """
    repo = DatasetRepository(db, tenant_id)
    ds = repo.list_by_source(source_id)
    return [DatasetSchema(id=d.id, name=d.name) for d in ds]


@router.get("/datasets/{dataset_id}/preview")
def dataset_preview(dataset_id: str, 
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
