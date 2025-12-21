"""
图像分类 - 业务逻辑
"""

import numpy as np
import torch
import torchvision.transforms as T
from PIL import Image

from .config import CLASSIFICATION_NAMES, IMG_SIZE
from .model import Classifier

# 全局模型实例
_model: Classifier = None
_device: torch.device = None


def init_model(model_path: str, device: torch.device):
    """初始化模型"""
    global _model, _device
    _device = device
    _model = Classifier()
    _model.load_state_dict(torch.load(model_path, map_location=device))
    _model.to(device)
    _model.eval()
    # print(f"分类模型加载完毕 (device: {device})")


def get_model() -> Classifier:
    """获取模型实例"""
    if _model is None:
        raise RuntimeError("模型未初始化，请先调用 init_model()")
    return _model


def preprocess_image(image: Image.Image) -> torch.Tensor:
    """图像预处理"""
    transform = T.Compose([T.Resize(IMG_SIZE), T.ToTensor()])
    return transform(image)


def classify_image(image: Image.Image) -> str:
    """
    执行图像分类

    Args:
        image: PIL 图像

    Returns:
        分类结果文本
    """
    model = get_model()

    # 预处理
    image_tensor = preprocess_image(image.convert("RGB"))
    input_batch = image_tensor.unsqueeze(0).to(_device)

    # 推理
    with torch.no_grad():
        output = model(input_batch)
        pred_idx = np.argmax(output.cpu().detach().numpy())

    return CLASSIFICATION_NAMES.get(pred_idx, "未知")
