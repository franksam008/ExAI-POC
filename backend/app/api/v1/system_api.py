# app/api/v1/system_api.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infra.db import SessionLocal
from app.infra.repositories.user_repo import UserRepository
from app.infra.repositories.audit_repo import AuditRepository

router = APIRouter(prefix="/system", tags=["system"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/users")
def list_users(db: Session = Depends(get_db)):
    repo = UserRepository(db)
    users = repo.list_all()
    return [{"id": u.id, "username": u.username, "created_at": u.created_at} for u in users]


@router.get("/audit-logs")
def list_audit_logs(db: Session = Depends(get_db)):
    repo = AuditRepository(db)
    logs = repo.list_recent()
    return [
        {
            "id": l.id,
            "user_id": l.user_id,
            "action": l.action,
            "detail": l.detail_json,
            "created_at": l.created_at,
        }
        for l in logs
    ]
