from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional
from enum import IntEnum

T = TypeVar("T")


class ApiCode(IntEnum):
    SUCCESS = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    VALIDATION_ERROR = 1001
    BUSINESS_ERROR = 2000
    SERVER_ERROR = 500


class Result(BaseModel, Generic[T]):
    """Unified response format"""
    code: int = Field(default=ApiCode.SUCCESS, description="Business status code")
    data: Optional[T] = Field(default=None, description="Data")
    message: str = Field(default="Success", description="Message")
