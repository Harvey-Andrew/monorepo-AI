"""商品标题分类模块

基于 BERT 的中文商品标题分类服务
"""

from .config import device
from .routes import router
from .startup import init_model

__all__ = [
    "router",
    "init_model",
    "device",
]
