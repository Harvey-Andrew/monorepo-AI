"""
AI 新闻分类与摘要 - 数据模型
"""

from pydantic import BaseModel, Field


class NewsInput(BaseModel):
    """新闻文本输入"""

    text: str = Field(..., description="新闻文本内容", min_length=10)


class ClassifyResponse(BaseModel):
    """分类响应"""

    category: str = Field(..., description="新闻分类结果")


class SummarizeResponse(BaseModel):
    """摘要响应"""

    summary: str = Field(..., description="新闻摘要")


class AnalyzeResponse(BaseModel):
    """综合分析响应（分类+摘要）"""

    category: str = Field(..., description="新闻分类结果")
    summary: str = Field(..., description="新闻摘要")
