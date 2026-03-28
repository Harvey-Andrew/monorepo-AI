"""
地址对齐 - 模型初始化模块
"""

from transformers import BertForTokenClassification, BertTokenizerFast

from .config import FINETUNED_DIR, device
from .model import AddressPredictor
from .service import init_predictor


def init_model():
    """初始化地址对齐模型"""
    print(f"[Address Alignment] Using device: {device}")

    # 检查模型目录
    model_path = FINETUNED_DIR / "best"
    if not model_path.exists():
        print(f"[Address Alignment] Warning: finetuned model not found - {model_path}")
        print("[Address Alignment] Please run training first to generate the model")
        return

    try:
        print("[Address Alignment] Loading model...")
        model = BertForTokenClassification.from_pretrained(str(model_path))
        tokenizer = BertTokenizerFast.from_pretrained(str(model_path))

        predictor = AddressPredictor(model=model, tokenizer=tokenizer, device=device)
        init_predictor(predictor)

        print("[Address Alignment] Model loaded successfully")
    except Exception as e:
        print(f"[Address Alignment] Failed to load model: {e}")
