"""
相似检索 - 配置文件
"""

from pathlib import Path

# 目录路径
_CURRENT_DIR = Path(__file__).parent
_PROJECT_DIR = _CURRENT_DIR.parent  # image-processing
_APPS_DIR = _PROJECT_DIR.parent  # apps
_BACKEND_DIR = _APPS_DIR.parent  # backend
_ROOT_DIR = _BACKEND_DIR.parent  # monorepo root

# 存储根目录
_STORAGE_DIR = _BACKEND_DIR / "storage" / "image-processing"

# 数据目录路径
IMG_PATH = _STORAGE_DIR / "dataset"

# 图像预处理配置
IMG_H = 64  # 输入图像高度
IMG_W = 64  # 输入图像宽度
IMG_SIZE = (IMG_H, IMG_W)

# 随机性相关配置
SEED = 42
TRAIN_RATIO = 0.75
TEST_RATIO = 1 - TRAIN_RATIO

# 训练超参数
LEARNING_RATE = 1e-3
TRAIN_BATCH_SIZE = 32
VAL_BATCH_SIZE = 32
TEST_BATCH_SIZE = 32
FULL_BATCH_SIZE = 32  # 全数据集批大小（生成嵌入用）
EPOCHS = 30

# 模型文件路径 - 保存到 storage/checkpoint 目录
CHECKPOINT_DIR = _STORAGE_DIR / "checkpoint"
ENCODER_MODEL_PATH = CHECKPOINT_DIR / "encoder.pt"
DECODER_MODEL_PATH = CHECKPOINT_DIR / "decoder.pt"
EMBEDDING_PATH = CHECKPOINT_DIR / "embeddings.npy"

# TensorBoard 日志目录
RUNS_DIR = _STORAGE_DIR / "runs" / "similarity_experiment"
