"""
AI 新闻分类与摘要 - 配置模块
"""

from pathlib import Path

import torch

# 设备检测
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 目录路径
STORAGE_DIR = Path(__file__).parent.parent.parent / "storage" / "ai-news"
PRETRAINED_DIR = STORAGE_DIR / "pretrained" / "bart-base-chinese"
FINETUNED_DIR = STORAGE_DIR / "finetuned"

# 分类类别列表
CATEGORY_LIST = ["财经", "社会", "教育", "科技", "时政", "体育", "游戏"]

# 模型配置
MAX_INPUT_LENGTH = 1024
MAX_OUTPUT_LENGTH = 128
NUM_BEAMS = 4
