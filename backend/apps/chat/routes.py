"""
Chat API Routes
"""

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from common.schemas import ApiCode, Result

from .schemas import ChatRequest, ChatResponse
from .service import chat_complete, chat_stream

router = APIRouter(prefix="/chat", tags=["AI聊天"])


@router.post("")
async def chat(request: ChatRequest):
    """
    AI聊天接口

    - stream=true: 返回SSE流式响应
    - stream=false: 返回完整JSON响应
    """
    if request.stream:
        return StreamingResponse(
            chat_stream(request.messages),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )
    else:
        content = await chat_complete(request.messages)
        return Result(
            code=ApiCode.SUCCESS,
            data=ChatResponse(content=content),
            message="Success",
        )


@router.get("/health")
async def health():
    """聊天服务健康检查"""
    from .config import GOOGLE_API_KEY

    return Result(
        code=ApiCode.SUCCESS,
        data={
            "status": "healthy",
            "api_key_configured": bool(GOOGLE_API_KEY),
        },
        message="Chat service is running",
    )
