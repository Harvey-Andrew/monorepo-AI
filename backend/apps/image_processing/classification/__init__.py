"""图像分类模块"""

from .model import Classifier
from .service import classify_image, init_model

__all__ = [
    "init_model",
    "classify_image",
    "Classifier",
]
