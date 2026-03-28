"""
AI 新闻分类与摘要 - 预测器模块

基于 BART 的中文新闻分类和摘要生成预测器
"""

import torch
import torch.nn as nn
from transformers import AutoConfig, AutoTokenizer, BartModel

from .config import (
    CATEGORY_LIST,
    MAX_INPUT_LENGTH,
    MAX_OUTPUT_LENGTH,
    NUM_BEAMS,
)


class ClassifyPredictor:
    """新闻分类预测器

    基于 BART Encoder 的分类模型
    """

    def __init__(self, model, tokenizer, device):
        """
        初始化预测器

        Args:
            model: 分类模型
            tokenizer: 分词器
            device: 计算设备 (cuda/cpu)
        """
        self.model = model.to(device)
        self.tokenizer = tokenizer
        self.device = device
        self.model.eval()

    @torch.inference_mode()
    def predict(self, texts: str | list) -> str | list:
        """
        预测新闻分类

        Args:
            texts: 单个文本或文本列表

        Returns:
            分类标签（单个或列表）
        """
        is_str = isinstance(texts, str)
        if is_str:
            texts = [texts]

        inputs = self.tokenizer(
            texts,
            max_length=MAX_INPUT_LENGTH,
            padding=True,
            truncation=True,
            return_tensors="pt",
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        outputs = self.model(**inputs)
        preds = torch.argmax(outputs["logits"], dim=-1).tolist()
        labels = [CATEGORY_LIST[pred_id] for pred_id in preds]

        return labels[0] if is_str else labels


class SummarizePredictor:
    """新闻摘要预测器

    基于完整 BART Encoder-Decoder 的 Seq2Seq 模型
    """

    def __init__(self, model, tokenizer, device):
        """
        初始化预测器

        Args:
            model: 摘要模型
            tokenizer: 分词器
            device: 计算设备 (cuda/cpu)
        """
        self.model = model.to(device)
        self.tokenizer = tokenizer
        self.device = device
        self.config = model.config
        self.model.eval()

    @torch.inference_mode()
    def predict(self, texts: str | list, batch_size: int = 4) -> str | list:
        """
        生成新闻摘要

        Args:
            texts: 单个文本或文本列表
            batch_size: 批处理大小

        Returns:
            摘要文本（单个或列表）
        """
        is_str = isinstance(texts, str)
        if is_str:
            texts = [texts]

        results = []
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i : i + batch_size]
            inputs = self.tokenizer(
                batch_texts,
                max_length=MAX_INPUT_LENGTH,
                padding=True,
                truncation=True,
                return_tensors="pt",
            ).to(self.device)

            # 使用 beam search 生成
            generated_ids = self._beam_search(
                inputs["input_ids"],
                inputs["attention_mask"],
                max_length=MAX_OUTPUT_LENGTH,
                num_beams=NUM_BEAMS,
            )

            # 解码生成的文本
            summaries = self.tokenizer.batch_decode(
                generated_ids, skip_special_tokens=True
            )
            results.extend(summaries)

        return results[0] if is_str else results

    def _beam_search(self, input_ids, attention_mask, max_length, num_beams):
        """束搜索解码"""
        device = input_ids.device
        batch_size = input_ids.size(0)
        vocab_size = self.config.vocab_size

        # 编码器前向传播
        encoder_outputs = self.model.model.encoder(input_ids, attention_mask)

        # 复制编码器输出以匹配 beam 数量
        encoder_hidden_states = encoder_outputs.last_hidden_state.repeat_interleave(
            num_beams, dim=0
        )
        encoder_attention_mask = attention_mask.repeat_interleave(num_beams, dim=0)

        # 初始化解码输入为起始符
        decoder_input_ids = torch.full(
            (batch_size * num_beams, 1),
            self.config.decoder_start_token_id,
            dtype=torch.long,
            device=device,
        )

        # 初始化 beam 分数
        beam_offset = torch.arange(batch_size, device=device) * num_beams
        beam_scores = torch.full((batch_size * num_beams,), -1e9, device=device)
        beam_scores[beam_offset] = 0

        done = torch.zeros(batch_size * num_beams, dtype=torch.bool, device=device)

        for step in range(max_length):
            decoder_outputs = self.model.model.decoder(
                input_ids=decoder_input_ids,
                encoder_hidden_states=encoder_hidden_states,
                encoder_attention_mask=encoder_attention_mask,
                use_cache=False,
            )

            logits = self.model.lm_head(decoder_outputs.last_hidden_state[:, -1, :])
            log_probs = nn.functional.log_softmax(logits, dim=-1)

            log_probs[done] = -float("inf")
            log_probs[done, self.config.eos_token_id] = 0

            log_probs = log_probs + beam_scores.unsqueeze(1)
            log_probs = log_probs.view(batch_size, num_beams * vocab_size)

            beam_scores, indices = torch.topk(log_probs, num_beams, dim=1)
            beam_scores = beam_scores.view(-1)

            beam_indices = (indices // vocab_size).view(-1)
            beam_indices = beam_indices + beam_offset.repeat_interleave(num_beams)
            token_ids = (indices % vocab_size).view(-1, 1)

            decoder_input_ids = torch.cat(
                [decoder_input_ids[beam_indices], token_ids], dim=1
            )

            done = (
                token_ids.squeeze(-1).eq(self.config.eos_token_id) | done[beam_indices]
            )
            if done.all():
                break

        # 选择分数最高的 beam
        beam_scores = beam_scores.view(batch_size, num_beams)
        best_indices = beam_scores.argmax(dim=-1) + beam_offset
        return decoder_input_ids[best_indices]


class ClassifyModel(nn.Module):
    """分类模型：BART Encoder + Linear Classifier"""

    def __init__(self, pretrained_path: str):
        super().__init__()
        self.tokenizer = AutoTokenizer.from_pretrained(pretrained_path)
        self.encoder = BartModel.from_pretrained(pretrained_path).encoder
        self.classifier = nn.Linear(self.encoder.config.hidden_size, len(CATEGORY_LIST))

        # 初始化分类器权重
        init_std = getattr(self.encoder.config, "init_std", 0.02)
        self.classifier.weight.data.normal_(mean=0.0, std=init_std)
        if self.classifier.bias is not None:
            self.classifier.bias.data.zero_()

        self.loss_fn = nn.CrossEntropyLoss()

    def forward(self, input_ids, attention_mask=None, labels=None):
        output = self.encoder(input_ids=input_ids, attention_mask=attention_mask)
        cls_hidden = output.last_hidden_state[:, 0, :]
        logits = self.classifier(cls_hidden)
        loss = self.loss_fn(logits, labels) if labels is not None else None
        return {"loss": loss, "logits": logits}

    def load_params(self, path):
        """加载微调后的参数"""
        self.load_state_dict(torch.load(path, map_location="cpu"))


class SummarizeModel(nn.Module):
    """摘要模型：完整的 BART Encoder-Decoder + LM Head"""

    def __init__(self, pretrained_path: str):
        super().__init__()
        self.config = AutoConfig.from_pretrained(pretrained_path)
        self.tokenizer = AutoTokenizer.from_pretrained(pretrained_path)
        self.model = BartModel.from_pretrained(pretrained_path)
        self.lm_head = nn.Linear(self.config.d_model, self.config.vocab_size)

        # 权重共享
        self.lm_head.weight = self.model.shared.weight

        self.loss_fn = nn.CrossEntropyLoss(ignore_index=-100)

    def forward(self, input_ids, attention_mask=None, labels=None):
        decoder_input_ids = None
        decoder_attention_mask = None

        if labels is not None:
            decoder_input_ids = labels.new_zeros(labels.shape)
            decoder_input_ids[:, 1:] = labels[:, :-1].clone()
            decoder_input_ids[:, 0] = self.config.decoder_start_token_id
            decoder_input_ids.masked_fill_(
                decoder_input_ids == -100, self.config.pad_token_id
            )
            decoder_attention_mask = (
                decoder_input_ids != self.config.pad_token_id
            ).long()

        encoder_outputs = self.model.encoder(input_ids, attention_mask)
        outputs = self.model.decoder(
            input_ids=decoder_input_ids,
            attention_mask=decoder_attention_mask,
            encoder_hidden_states=encoder_outputs.last_hidden_state,
            encoder_attention_mask=attention_mask,
            use_cache=False,
        )

        logits = self.lm_head(outputs.last_hidden_state)

        loss = None
        if labels is not None:
            loss = self.loss_fn(
                logits.view(-1, self.config.vocab_size), labels.view(-1)
            )

        return {"loss": loss, "logits": logits}

    def load_params(self, path):
        """加载微调后的参数"""
        self.load_state_dict(torch.load(path, map_location="cpu"))
