"""
商品标题分类 - 数据模型
"""

from pydantic import BaseModel, Field


class TextInput(BaseModel):
    """文本输入请求体"""

    text: str = Field(..., description="商品标题文本", min_length=1)


class BatchTextInput(BaseModel):
    """批量文本输入请求体"""

    texts: list[str] = Field(..., description="商品标题文本列表", min_length=1)


class ClassificationResponse(BaseModel):
    """分类响应"""

    category: str = Field(..., description="分类结果")


class BatchClassificationResponse(BaseModel):
    """批量分类响应"""

    categories: list[str] = Field(..., description="分类结果列表")
