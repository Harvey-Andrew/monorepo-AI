"""
Chat Service - Gemini API Integration
"""

import json
from collections.abc import AsyncGenerator

from google import genai
from google.genai import types

from .schemas import ChatMessage

# 延迟初始化 - 避免配置缓存问题
_client = None


def get_client():
    """获取或创建 Gemini client"""
    global _client
    if _client is None:
        from .config import GOOGLE_API_KEY

        if GOOGLE_API_KEY:
            _client = genai.Client(api_key=GOOGLE_API_KEY)
    return _client


def get_model_name():
    """获取模型名称"""
    from .config import MODEL_NAME

    return MODEL_NAME


def get_default_system_prompt():
    """获取默认系统提示"""
    from .config import DEFAULT_SYSTEM_PROMPT

    return DEFAULT_SYSTEM_PROMPT


def convert_to_gemini_history(
    messages: list[ChatMessage],
) -> list[types.Content]:
    """将消息转换为Gemini格式"""
    history = []
    for msg in messages:
        if msg.role == "system":
            continue  # System prompt handled separately
        role = "user" if msg.role == "user" else "model"
        history.append(types.Content(role=role, parts=[types.Part(text=msg.content)]))
    return history


def get_system_instruction(messages: list[ChatMessage]) -> str:
    """提取system prompt"""
    for msg in messages:
        if msg.role == "system":
            return msg.content
    return get_default_system_prompt()


async def chat_stream(messages: list[ChatMessage]) -> AsyncGenerator[str, None]:
    """
    流式聊天 - 使用SSE格式返回

    Yields:
        SSE格式的数据块: data: {"content": "...", "done": false}
    """
    client = get_client()
    if not client:
        error_msg = (
            "API Key未配置。请按以下步骤操作：\n"
            "1. 访问 https://aistudio.google.com/apikey 获取API Key\n"
            "2. 停止当前服务 (Ctrl+C)\n"
            "3. 设置环境变量: $env:GOOGLE_API_KEY='你的Key'\n"
            "4. 重新启动: pnpm dev"
        )
        yield f"data: {json.dumps({'error': error_msg}, ensure_ascii=False)}\n\n"
        yield 'data: {"done": true}\n\n'
        return

    try:
        # 准备消息
        system_instruction = get_system_instruction(messages)
        history = convert_to_gemini_history(messages[:-1])
        user_message = messages[-1].content if messages else ""

        # 创建聊天并发送消息
        response = client.models.generate_content_stream(
            model=get_model_name(),
            contents=history
            + [types.Content(role="user", parts=[types.Part(text=user_message)])],
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
            ),
        )

        # 流式返回
        for chunk in response:
            if chunk.text:
                data = json.dumps(
                    {"content": chunk.text, "done": False}, ensure_ascii=False
                )
                yield f"data: {data}\n\n"

        yield 'data: {"content": "", "done": true}\n\n'

    except Exception as e:
        error_msg = json.dumps({"error": str(e), "done": True}, ensure_ascii=False)
        yield f"data: {error_msg}\n\n"


async def chat_complete(messages: list[ChatMessage]) -> str:
    """
    非流式聊天 - 一次性返回完整响应
    """
    client = get_client()
    if not client:
        return (
            "API Key未配置。请按以下步骤操作：\n"
            "1. 访问 https://aistudio.google.com/apikey 获取API Key\n"
            "2. 停止当前服务 (Ctrl+C)\n"
            "3. 设置环境变量: $env:GOOGLE_API_KEY='你的Key'\n"
            "4. 重新启动: pnpm dev"
        )

    try:
        system_instruction = get_system_instruction(messages)
        history = convert_to_gemini_history(messages[:-1])
        user_message = messages[-1].content if messages else ""

        response = client.models.generate_content(
            model=get_model_name(),
            contents=history
            + [types.Content(role="user", parts=[types.Part(text=user_message)])],
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
            ),
        )

        return response.text or ""

    except Exception as e:
        return f"Error: {e!s}"
