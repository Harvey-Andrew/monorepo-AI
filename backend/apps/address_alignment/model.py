"""
地址对齐 - 预测器模块

基于 BERT 的中文地址序列标注预测器
"""

import re

import pymysql
import torch
from rapidfuzz import fuzz

from .config import LABELS, MAX_INPUT_LENGTH


class AddressPredictor:
    """地址序列标注预测器"""

    def __init__(self, model, tokenizer, device):
        """
        初始化预测器

        Args:
            model: 序列标注模型
            tokenizer: 分词器
            device: 计算设备 (cuda/cpu)
        """
        self.model = model.to(device)
        self.tokenizer = tokenizer
        self.device = device
        self.model.eval()

    @torch.inference_mode()
    def predict_tags(
        self, texts: str | list, batch_size: int = 64
    ) -> list | list[list]:
        """
        预测序列标签

        Args:
            texts: 单个文本或文本列表
            batch_size: 批处理大小

        Returns:
            标签列表（单个或列表的列表）
        """
        is_str = isinstance(texts, str)
        if is_str:
            texts = [texts]

        results = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            batch_words = [list(t.replace(" ", "")) for t in batch]

            tokenized = self.tokenizer(
                batch_words,
                max_length=MAX_INPUT_LENGTH,
                truncation=True,
                padding=True,
                return_tensors="pt",
                is_split_into_words=True,
            ).to(self.device)

            outputs = self.model(tokenized["input_ids"], tokenized["attention_mask"])
            preds = torch.argmax(outputs["logits"], dim=-1).detach().cpu()

            # 过滤 [CLS] 和 [SEP] 的预测
            filtered_preds = [
                [
                    LABELS[label_seq[j + 1].item()]
                    for j in tokenized.word_ids(batch_index=idx)
                    if j is not None
                ]
                for idx, label_seq in enumerate(preds)
            ]

            # 将原始空格位置标注为 'O'
            filled_preds = []
            for string, labels in zip(batch, filtered_preds):
                labels_iter = iter(labels)
                filled_preds.append(
                    [next(labels_iter) if char != " " else "O" for char in string]
                )
            results.extend(filled_preds)

        return results[0] if is_str else results

    def extract_address(self, text: str, tags: list[str]) -> dict[str, str | None]:
        """
        从标签中提取地址实体

        Args:
            text: 原始文本
            tags: 预测的标签序列

        Returns:
            结构化地址字典
        """
        # 去掉 B/I/E/S 前缀
        tags = [i[2:] if len(i) > 2 else "" for i in tags]

        address: dict[str, str | None] = {
            "prov": None,
            "city": None,
            "district": None,
            "town": None,
            "detail": None,
            "name": None,
            "phone": None,
        }

        start_pos = 0
        tag_len = len(tags)
        for end_pos in range(tag_len):
            if (end_pos == tag_len - 1) or (tags[end_pos + 1] != tags[start_pos]):
                if tags[start_pos] != "":
                    address[tags[start_pos]] = text[start_pos : end_pos + 1]
                start_pos = end_pos + 1

        return address

    def check_address(
        self, text: str, address: dict[str, str | None], mysql_config: dict
    ) -> dict[str, str | None]:
        """
        通过数据库校验和编辑距离匹配优化地址

        Args:
            text: 原始文本
            address: 提取的地址
            mysql_config: MySQL 配置

        Returns:
            校验后的地址
        """
        # 检查电话号码格式
        if address["phone"]:
            phone = address["phone"]
            if not (len(phone) == 11 and phone.isdigit() and phone[0] == "1"):
                pattern = r"^(?:\+?\d{1,4}[-.\\s]?)?(\(?\d{2,4}\)?[-.\\s]?)?\d{6,11}$"
                if not re.match(pattern, phone):
                    address["phone"] = None

        # 如果地址部分全为空则返回
        if all(address[k] is None for k in ["prov", "city", "district", "town"]):
            return address

        def flatten_address_tree(tree, chain=None):
            """将地址树展平"""
            if chain is None:
                chain = []
            chains = []
            if isinstance(tree, dict) and tree:
                for k, v in tree.items():
                    chains.extend(flatten_address_tree(v, chain + [k]))
            elif isinstance(tree, list) and tree:
                for road in tree:
                    chains.append(chain + [road])
            else:
                chains.append(chain)
            return chains

        region_type_ids = [2, 3, 4, 5]
        region_type_names = ["prov", "city", "district", "town"]

        try:
            with pymysql.connect(**mysql_config) as mysql_conn:
                with mysql_conn.cursor(pymysql.cursors.DictCursor) as cursor:
                    params_list = [
                        (i, address[k])
                        for i, k in zip(region_type_ids, region_type_names)
                    ]
                    params_list.extend(
                        [
                            (2, address["city"]),
                            (3, address["prov"]),
                            (3, address["district"]),
                        ]
                    )
                    params_list = [(i[0], f"%{i[1]}%") for i in params_list if i[1]]

                    if not params_list:
                        return address

                    placeholders = "(region_type=%s and name like %s)"
                    sql = (
                        f"select full_name from region where {placeholders}"
                        + f" or {placeholders}" * (len(params_list) - 1)
                    )
                    params = [i for pair in params_list for i in pair]
                    cursor.execute(sql, params)
                    rows = cursor.fetchall()
                    prefixes = [row["full_name"].split(" ") for row in rows]

            # 构建地址树
            address_tree = {}
            leaf_id = region_type_ids[-1] - region_type_ids[0]
            for prefix in prefixes:
                node = address_tree
                for i in range(len(prefix)):
                    if i == leaf_id:
                        node.append(prefix[i])
                    elif i == leaf_id - 1:
                        node = node.setdefault(prefix[i], [])
                    else:
                        node = node.setdefault(prefix[i], {})

            # 展平并计算相似度
            address_chains = flatten_address_tree(address_tree)
            address_texts = ["".join(i) for i in address_chains]
            scores = [fuzz.ratio(i, text) for i in address_texts]

            # 取最佳匹配
            if scores:
                correct_address = dict.fromkeys(region_type_names)
                correct_address_chain = address_chains[scores.index(max(scores))]
                correct_address.update(zip(region_type_names, correct_address_chain))
                return correct_address

        except Exception as e:
            print(f"[Address Alignment] Database check failed: {e}")

        return address

    def align_address(
        self, text: str, mysql_config: dict | None = None
    ) -> dict[str, str | None]:
        """
        完整的地址对齐流程

        Args:
            text: 原始地址文本
            mysql_config: MySQL 配置（可选）

        Returns:
            结构化地址字典
        """
        # 序列标注
        tags = self.predict_tags(text)
        # 提取地址实体
        address = self.extract_address(text, tags)
        # 数据库校验（如果配置了）
        if mysql_config:
            correct_address = self.check_address(text, address, mysql_config)
            address.update(correct_address)
        return address
