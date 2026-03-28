"""
地址对齐 - 配置模块
"""

from pathlib import Path

import torch

# 设备检测
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 目录路径
STORAGE_DIR = Path(__file__).parent.parent.parent / "storage" / "address-alignment"
PRETRAINED_DIR = (
    STORAGE_DIR / "pretrained" / "roberta-small-wwm-chinese-cluecorpussmall"
)
FINETUNED_DIR = STORAGE_DIR / "finetuned"

# MySQL 配置（用于地址校验）
MYSQL_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "abc123456",
    "database": "region",
    "charset": "utf8mb4",
}

# 模型配置
MAX_INPUT_LENGTH = 128

# BIOES 标签体系（26类）
LABELS = [
    "O",
    "B-prov",
    "I-prov",
    "E-prov",
    "B-city",
    "I-city",
    "E-city",
    "B-district",
    "I-district",
    "E-district",
    "S-district",
    "B-town",
    "I-town",
    "E-town",
    "S-town",
    "B-detail",
    "I-detail",
    "E-detail",
    "S-detail",
    "B-name",
    "I-name",
    "E-name",
    "B-phone",
    "I-phone",
    "E-phone",
]
