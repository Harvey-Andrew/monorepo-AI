"""
Chat Module Schemas
"""

from typing import Literal

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """聊天消息"""

    role: Literal["user", "assistant", "system"] = Field(description="消息角色")
    content: str = Field(description="消息内容")


class ChatRequest(BaseModel):
    """聊天请求"""

    messages: list[ChatMessage] = Field(description="消息历史")
    stream: bool = Field(default=True, description="是否流式返回")


class ChatResponse(BaseModel):
    """聊天响应（非流式）"""

    content: str = Field(description="回复内容")
    finish_reason: str | None = Field(default=None, description="结束原因")
