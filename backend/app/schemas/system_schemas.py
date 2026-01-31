# app/schemas/system_schemas.py
from pydantic import BaseModel
from datetime import datetime

class UserSchema(BaseModel):
    id: str
    username: str
    created_at: datetime


class AuditLogSchema(BaseModel):
    id: int
    user_id: str
    action: str
    detail: str
    created_at: datetime
