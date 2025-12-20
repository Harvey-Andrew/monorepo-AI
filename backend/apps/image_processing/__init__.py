"""Image Processing 项目

包含图像去噪、分类、相似检索三个模块
"""

from .routes import router
from .startup import init_all_models, device

__all__ = [
    "router",
    "init_all_models",
    "device",
]

