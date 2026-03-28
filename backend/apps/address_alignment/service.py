"""
地址对齐 - 业务逻辑层
"""

from .config import MYSQL_CONFIG
from .model import AddressPredictor

# 全局预测器实例
_predictor: AddressPredictor = None


def init_predictor(predictor: AddressPredictor):
    """初始化预测器"""
    global _predictor
    _predictor = predictor


def get_predictor() -> AddressPredictor:
    """获取预测器实例"""
    if _predictor is None:
        raise RuntimeError("预测器未初始化，请先调用 init_predictor()")
    return _predictor


def is_ready() -> bool:
    """检查服务是否就绪"""
    return _predictor is not None


def predict_tags(text: str) -> list[str]:
    """
    预测序列标签

    Args:
        text: 地址文本

    Returns:
        每个字符的标签列表
    """
    predictor = get_predictor()
    return predictor.predict_tags(text)


def align_address(text: str, use_db_check: bool = True) -> dict[str, str | None]:
    """
    地址对齐（提取+校验）

    Args:
        text: 地址文本
        use_db_check: 是否使用数据库校验

    Returns:
        结构化地址字典
    """
    predictor = get_predictor()
    mysql_config = MYSQL_CONFIG if use_db_check else None
    return predictor.align_address(text, mysql_config)


def extract_address(text: str) -> dict[str, str | None]:
    """
    仅提取地址（不使用数据库校验）

    Args:
        text: 地址文本

    Returns:
        结构化地址字典
    """
    predictor = get_predictor()
    tags = predictor.predict_tags(text)
    return predictor.extract_address(text, tags)
