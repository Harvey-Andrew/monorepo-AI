"""
商品标题分类 - 模型初始化模块
"""

from transformers import AutoModelForSequenceClassification, AutoTokenizer

from .config import BERT_MODEL_NAME, MODEL_DIR, device
from .model import Predictor
from .service import init_predictor


def init_model():
    """初始化商品分类模型"""
    print(f"[Product Classification] Using device: {device}")

    if not MODEL_DIR.exists():
        print(f"Warning: model directory not found - {MODEL_DIR}")
        return

    try:
        # 加载分词器
        tokenizer = AutoTokenizer.from_pretrained(BERT_MODEL_NAME)

        # 加载微调后的模型
        model = AutoModelForSequenceClassification.from_pretrained(str(MODEL_DIR))

        # 创建预测器并注册到服务层
        predictor = Predictor(model=model, tokenizer=tokenizer, device=device)
        init_predictor(predictor)

        print("[Product Classification] Model loaded successfully")
    except Exception as e:
        print(f"[Product Classification] Failed to load model: {e}")
