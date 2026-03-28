"""地址对齐模块

基于 BERT 的中文地址序列标注和结构化提取服务
"""

from .config import device
from .routes import router
from .startup import init_model

__all__ = [
    "router",
    "init_model",
    "device",
]
