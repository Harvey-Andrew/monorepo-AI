"""图像分类模块"""

from .service import init_model, classify_image
from .model import Classifier

__all__ = [
    "init_model",
    "classify_image",
    "Classifier",
]
