"""
Image Processing - 模型初始化模块

统一初始化所有图像处理相关模型
"""

from pathlib import Path
import torch

# 检测设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 模型存储目录
STORAGE_DIR = Path(__file__).parent.parent.parent / "storage" / "image-processing" / "checkpoint"


def init_all_models():
    """初始化所有模型"""
    print(f"Using device: {device}")
    
    # 去噪模型
    from .denoising import init_model as init_denoising
    denoiser_path = STORAGE_DIR / "denoiser.pt"
    if denoiser_path.exists():
        init_denoising(str(denoiser_path), device)
    else:
        print(f"Warning: denoiser model not found - {denoiser_path}")

    # 分类模型
    from .classification import init_model as init_classification
    classifier_path = STORAGE_DIR / "classifier.pt"
    if classifier_path.exists():
        init_classification(str(classifier_path), device)
    else:
        print(f"Warning: classifier model not found - {classifier_path}")

    # 相似度模型
    from .similarity import init_model as init_similarity
    encoder_path = STORAGE_DIR / "encoder.pt"
    embeddings_path = STORAGE_DIR / "embeddings.npy"
    if encoder_path.exists() and embeddings_path.exists():
        init_similarity(str(encoder_path), str(embeddings_path), device)
    else:
        print(f"Warning: similarity model not found")
