"""
AI 新闻分类与摘要 - 模型初始化模块
"""

from .config import FINETUNED_DIR, PRETRAINED_DIR, device
from .model import ClassifyModel, ClassifyPredictor, SummarizeModel, SummarizePredictor
from .service import init_classify_predictor, init_summarize_predictor


def init_model():
    """初始化 AI 新闻模型"""
    print(f"[AI News] Using device: {device}")

    # 检查预训练模型
    if not PRETRAINED_DIR.exists():
        print(f"[AI News] Warning: pretrained model not found - {PRETRAINED_DIR}")
        print("[AI News] Please copy bart-base-chinese to storage/ai-news/pretrained/")
        return

    # 初始化分类模型
    classify_model_path = FINETUNED_DIR / "classify.pt"
    if classify_model_path.exists():
        try:
            print("[AI News] Loading classify model...")
            model = ClassifyModel(str(PRETRAINED_DIR))
            model.load_params(str(classify_model_path))
            predictor = ClassifyPredictor(
                model=model, tokenizer=model.tokenizer, device=device
            )
            init_classify_predictor(predictor)
            print("[AI News] Classify model loaded successfully")
        except Exception as e:
            print(f"[AI News] Failed to load classify model: {e}")
    else:
        print(f"[AI News] Warning: classify model not found - {classify_model_path}")
        print("[AI News] Please run training first to generate the model")

    # 初始化摘要模型
    summarize_model_path = FINETUNED_DIR / "summarize.pt"
    if summarize_model_path.exists():
        try:
            print("[AI News] Loading summarize model...")
            model = SummarizeModel(str(PRETRAINED_DIR))
            model.load_params(str(summarize_model_path))
            predictor = SummarizePredictor(
                model=model, tokenizer=model.tokenizer, device=device
            )
            init_summarize_predictor(predictor)
            print("[AI News] Summarize model loaded successfully")
        except Exception as e:
            print(f"[AI News] Failed to load summarize model: {e}")
    else:
        print(f"[AI News] Warning: summarize model not found - {summarize_model_path}")
        print("[AI News] Please run training first to generate the model")
