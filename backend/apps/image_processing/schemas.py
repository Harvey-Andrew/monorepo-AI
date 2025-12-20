"""
Image Processing - Unified Data Models
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Any


# Classification Schemas
class ClassificationRequest(BaseModel):
    """分类请求"""
    image: Any = Field(..., description="上传的图片文件")


class ClassificationResponse(BaseModel):
    """分类响应"""
    result: str = Field(..., description="分类结果")


# Denoising Schemas
class DenoisingRequest(BaseModel):
    """去噪请求（用于文档，实际使用 FormData）"""
    image: Any = Field(..., description="上传的图片文件")


class DenoisingResponse(BaseModel):
    """去噪响应"""
    noisy_img: str = Field(..., description="添加噪声后的图像 (base64)")
    denoised_image: str = Field(..., description="去噪后的图像 (base64)")


# Similarity Schemas
class SimilarityRequest(BaseModel):
    """相似检索请求"""
    image: Any = Field(..., description="上传的图片文件")
    num_images: int = Field(default=10, description="相似图片数量")


class SimilarityResponse(BaseModel):
    """相似检索响应"""
    image_urls: List[str] = Field(..., description="相似图像 URL 列表")
