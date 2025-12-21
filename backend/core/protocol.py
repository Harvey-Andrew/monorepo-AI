"""
协议定义

定义通用的 Pydantic 数据模型，用于类型生成
"""

from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    """基础响应模型"""

    success: bool = True
    message: str | None = None


class ImageRequest(BaseModel):
    """图像请求基类（用于文档，实际使用 FormData）"""

    pass


class DenoisingResponse(BaseModel):
    """去噪响应"""

    noisy_img: str = Field(..., description="添加噪声后的图像 (base64)")
    denoised_image: str = Field(..., description="去噪后的图像 (base64)")


class ClassificationResponse(BaseModel):
    """分类响应"""

    result: str = Field(..., description="分类结果")


class SimilarityResponse(BaseModel):
    """相似检索响应"""

    indices_list: list[int] = Field(..., description="相似图像索引列表")
    image_urls: list[str] = Field(..., description="相似图像 URL 列表")


class ErrorResponse(BaseModel):
    """错误响应"""

    success: bool = False
    error: str = Field(..., description="错误信息")
    detail: str | None = None
