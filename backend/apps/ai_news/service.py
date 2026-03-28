"""
AI 新闻分类与摘要 - 业务逻辑层
"""

from .model import ClassifyPredictor, SummarizePredictor

# 全局预测器实例
_classify_predictor: ClassifyPredictor = None
_summarize_predictor: SummarizePredictor = None


def init_classify_predictor(predictor: ClassifyPredictor):
    """初始化分类预测器"""
    global _classify_predictor
    _classify_predictor = predictor


def init_summarize_predictor(predictor: SummarizePredictor):
    """初始化摘要预测器"""
    global _summarize_predictor
    _summarize_predictor = predictor


def get_classify_predictor() -> ClassifyPredictor:
    """获取分类预测器实例"""
    if _classify_predictor is None:
        raise RuntimeError("分类预测器未初始化，请先调用 init_classify_predictor()")
    return _classify_predictor


def get_summarize_predictor() -> SummarizePredictor:
    """获取摘要预测器实例"""
    if _summarize_predictor is None:
        raise RuntimeError("摘要预测器未初始化，请先调用 init_summarize_predictor()")
    return _summarize_predictor


def is_classify_ready() -> bool:
    """检查分类服务是否就绪"""
    return _classify_predictor is not None


def is_summarize_ready() -> bool:
    """检查摘要服务是否就绪"""
    return _summarize_predictor is not None


def classify_news(text: str) -> str:
    """
    新闻分类

    Args:
        text: 新闻文本

    Returns:
        分类标签
    """
    predictor = get_classify_predictor()
    return predictor.predict(text)


def summarize_news(text: str) -> str:
    """
    新闻摘要

    Args:
        text: 新闻文本

    Returns:
        摘要文本
    """
    predictor = get_summarize_predictor()
    return predictor.predict(text)


def analyze_news(text: str) -> dict:
    """
    新闻综合分析（分类+摘要）

    Args:
        text: 新闻文本

    Returns:
        包含 category 和 summary 的字典
    """
    result = {}

    if is_classify_ready():
        result["category"] = classify_news(text)
    else:
        result["category"] = "模型未加载"

    if is_summarize_ready():
        result["summary"] = summarize_news(text)
    else:
        result["summary"] = "模型未加载"

    return result
