# app/core/exceptions.py
from fastapi import HTTPException

"""
自定义异常类型：
- POC：只定义一个业务异常
"""

class BusinessException(HTTPException):
    """
    业务异常：
    - 用于抛出可预期的业务错误
    """
    def __init__(self, status_code: int = 400, detail: str = "业务异常"):
        super().__init__(status_code=status_code, detail=detail)
