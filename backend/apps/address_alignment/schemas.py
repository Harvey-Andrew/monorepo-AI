"""
地址对齐 - 数据模型
"""

from pydantic import BaseModel, Field


class AddressInput(BaseModel):
    """地址输入"""

    text: str = Field(..., description="地址文本", min_length=5)


class AddressResponse(BaseModel):
    """结构化地址响应"""

    prov: str | None = Field(None, description="省份")
    city: str | None = Field(None, description="城市")
    district: str | None = Field(None, description="区/县")
    town: str | None = Field(None, description="街道/镇")
    detail: str | None = Field(None, description="详细地址")
    name: str | None = Field(None, description="姓名")
    phone: str | None = Field(None, description="电话")


class TaggingResponse(BaseModel):
    """序列标注响应"""

    text: str = Field(..., description="原始文本")
    tags: list[str] = Field(..., description="每个字符的标签")
