"""
商品标题分类 - 配置模块
"""

from pathlib import Path

import torch

# 设备检测
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 目录路径
STORAGE_DIR = Path(__file__).parent.parent.parent / "storage" / "product-classification"
MODEL_DIR = STORAGE_DIR / "best"

# 模型配置
BERT_MODEL_NAME = "google-bert/bert-base-chinese"
