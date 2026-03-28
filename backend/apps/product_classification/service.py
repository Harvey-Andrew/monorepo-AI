"""
商品标题分类 - 业务逻辑层
"""

from .model import Predictor

# 全局预测器实例
_predictor: Predictor = None


def init_predictor(predictor: Predictor):
    """初始化预测器"""
    global _predictor
    _predictor = predictor


def get_predictor() -> Predictor:
    """获取预测器实例"""
    if _predictor is None:
        raise RuntimeError("预测器未初始化，请先调用 init_predictor()")
    return _predictor


def classify_text(text: str) -> str:
    """
    分类商品标题

    Args:
        text: 商品标题文本

    Returns:
        分类标签
    """
    predictor = get_predictor()
    return predictor.predict(text)


def classify_texts(texts: list) -> list:
    """
    批量分类商品标题

    Args:
        texts: 商品标题列表

    Returns:
        分类标签列表
    """
    predictor = get_predictor()
    return predictor.predict(texts)
