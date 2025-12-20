"""
相似检索 - 业务逻辑
"""

import torch
import torchvision.transforms as T
import numpy as np
from PIL import Image
from typing import List, Tuple
from sklearn.neighbors import NearestNeighbors

from .config import IMG_SIZE
from .model import ConvEncoder

# 全局状态
_encoder: ConvEncoder = None
_embeddings: np.ndarray = None
_device: torch.device = None


def init_model(encoder_path: str, embeddings_path: str, device: torch.device):
    """初始化模型和嵌入矩阵"""
    global _encoder, _embeddings, _device
    _device = device

    # 加载编码器
    _encoder = ConvEncoder()
    _encoder.load_state_dict(torch.load(encoder_path, map_location=device))
    _encoder.to(device)
    _encoder.eval()
    print(f"相似检索编码器加载完毕 (device: {device})")

    # 加载嵌入矩阵
    _embeddings = np.load(embeddings_path)
    print(f"嵌入矩阵加载完毕 (shape: {_embeddings.shape})")


def get_encoder() -> ConvEncoder:
    """获取编码器实例"""
    if _encoder is None:
        raise RuntimeError("模型未初始化，请先调用 init_model()")
    return _encoder


def preprocess_image(image: Image.Image) -> torch.Tensor:
    """图像预处理"""
    transform = T.Compose([T.Resize(IMG_SIZE), T.ToTensor()])
    return transform(image)


def find_similar_images(
    image: Image.Image, num_images: int = 10
) -> Tuple[List[int], List[str]]:
    """
    查找相似图像

    Args:
        image: PIL 图像
        num_images: 返回的相似图像数量

    Returns:
        (indices_list, image_urls)
    """
    encoder = get_encoder()

    # 预处理
    image_tensor = preprocess_image(image.convert("RGB"))
    input_batch = image_tensor.unsqueeze(0).to(_device)

    # 编码
    with torch.no_grad():
        embedding = encoder(input_batch).cpu().numpy()

    # 展平为向量
    image_vector = embedding.reshape((embedding.shape[0], -1))

    # KNN 查找
    knn = NearestNeighbors(n_neighbors=num_images, metric="cosine")
    knn.fit(_embeddings)
    _, indices = knn.kneighbors(image_vector)

    indices_list = indices[0].tolist()
    image_urls = [f"/storage/image-processing/dataset/{idx}.jpg" for idx in indices_list]

    return indices_list, image_urls
