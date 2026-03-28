"""AI 新闻分类与摘要模块

基于 BART 的中文新闻分类（7类）和自动摘要生成服务
"""

from .config import device
from .routes import router
from .startup import init_model

__all__ = [
    "router",
    "init_model",
    "device",
]
