# app/core/security.py
from fastapi import Header, HTTPException

"""
安全相关逻辑：
- POC：不做真正 JWT 校验，只预留接口
"""

def verify_token(authorization: str | None = Header(default=None)) -> str:
    """
    伪 Token 校验：
    - 如果带了 Authorization，就认为是合法用户
    - 返回 user_id（POC 固定）
    """
    if authorization is None:
        # POC：不强制校验，生产环境应抛异常
        return "demo-user"
    # TODO: 解析 JWT，获取 user_id
    return "demo-user"
