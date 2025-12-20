"""
图像去噪 - 业务逻辑
"""

import torch
import torchvision.transforms as T
from PIL import Image
from io import BytesIO
import base64
from typing import Tuple

from .config import IMG_SIZE, NOISE_RATIO
from .model import ConvDenoiser

# 全局模型实例
_model: ConvDenoiser = None
_device: torch.device = None


def init_model(model_path: str, device: torch.device):
    """初始化模型"""
    global _model, _device
    _device = device
    _model = ConvDenoiser()
    _model.load_state_dict(torch.load(model_path, map_location=device))
    _model.to(device)
    _model.eval()
    print(f"去噪模型加载完毕 (device: {device})")


def get_model() -> ConvDenoiser:
    """获取模型实例"""
    if _model is None:
        raise RuntimeError("模型未初始化，请先调用 init_model()")
    return _model


def preprocess_image(image: Image.Image) -> torch.Tensor:
    """图像预处理"""
    transform = T.Compose([T.Resize(IMG_SIZE), T.ToTensor()])
    return transform(image)


def add_noise(image_tensor: torch.Tensor) -> torch.Tensor:
    """添加随机噪声"""
    noisy = image_tensor + NOISE_RATIO * torch.randn(*image_tensor.shape)
    return torch.clip(noisy, 0.0, 1.0)


def tensor_to_pil(tensor: torch.Tensor) -> Image.Image:
    """张量转 PIL 图像"""
    array = tensor.permute(1, 2, 0).numpy() * 255
    return Image.fromarray(array.astype("uint8"))


def encode_image(img: Image.Image) -> str:
    """图像编码为 base64"""
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def denoise_image(image: Image.Image) -> Tuple[str, str]:
    """
    执行图像去噪

    Args:
        image: PIL 图像

    Returns:
        (noisy_base64, denoised_base64)
    """
    model = get_model()

    # 预处理
    image_tensor = preprocess_image(image.convert("RGB"))
    noisy_tensor = add_noise(image_tensor)

    # 推理
    with torch.no_grad():
        input_batch = noisy_tensor.unsqueeze(0).to(_device)
        output = model(input_batch)
        denoised_tensor = output.squeeze(0).cpu()

    # 后处理
    noisy_pil = tensor_to_pil(noisy_tensor)
    denoised_pil = tensor_to_pil(denoised_tensor)

    return encode_image(noisy_pil), encode_image(denoised_pil)
