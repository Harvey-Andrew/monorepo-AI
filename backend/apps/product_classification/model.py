"""
商品标题分类 - 预测器模块

基于 BERT 的中文商品标题分类预测器
"""

import torch


class Predictor:
    """商品标题分类预测器"""

    def __init__(self, model, tokenizer, device):
        """
        初始化预测器

        Args:
            model: 预训练的分类模型
            tokenizer: 分词器
            device: 计算设备 (cuda/cpu)
        """
        self.model = model.to(device)
        self.tokenizer = tokenizer
        self.device = device
        self.model.eval()

    def predict(self, texts: str | list) -> str | list:
        """
        预测商品分类

        Args:
            texts: 单个文本或文本列表

        Returns:
            分类标签（单个或列表）
        """
        # 统一数据格式
        is_str = isinstance(texts, str)
        if is_str:
            texts = [texts]

        # 分词编码
        inputs = self.tokenizer(
            texts, padding=True, truncation=True, return_tensors="pt"
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        # 前向传播
        with torch.no_grad():
            outputs = self.model(**inputs)

        # 解码标签
        preds = torch.argmax(outputs.logits, dim=-1).tolist()
        labels = [self.model.config.id2label[pred_id] for pred_id in preds]

        if is_str:
            return labels[0]
        return labels
