# app/api/v1/auth_api.py
from fastapi import APIRouter
from app.schemas.auth_schemas import LoginRequest, LoginResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(req: LoginRequest):
    """
    登录接口：
    - POC：不校验密码，直接返回一个假 token
    """
    return LoginResponse(access_token="fake-token-for-" + req.username)
