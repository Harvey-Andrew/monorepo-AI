"""
相似检索 - 训练/测试引擎
"""

__all__ = ["train_epoch", "test_epoch", "create_embeddings", "compute_similar_images"]

import torch
import numpy as np
from sklearn.neighbors import NearestNeighbors


def train_epoch(encoder, decoder, train_loader, loss_fn, optimizer, device):
    """
    执行一轮训练

    Returns:
        平均训练损失
    """
    encoder.train()
    decoder.train()
    total_loss = 0

    for inputs, targets in train_loader:
        inputs, targets = inputs.to(device), targets.to(device)

        # 前向传播
        encoded_feature = encoder(inputs)
        outputs = decoder(encoded_feature)
        loss = loss_fn(outputs, targets)

        # 反向传播
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    return total_loss / len(train_loader)


def test_epoch(encoder, decoder, test_loader, loss_fn, device):
    """
    执行一次验证/测试

    Returns:
        平均损失
    """
    encoder.eval()
    decoder.eval()
    total_loss = 0

    with torch.no_grad():
        for inputs, targets in test_loader:
            inputs, targets = inputs.to(device), targets.to(device)

            # 前向传播
            encoded_feature = encoder(inputs)
            outputs = decoder(encoded_feature)
            loss = loss_fn(outputs, targets)

            # 累计损失
            total_loss += loss.item()

    return total_loss / len(test_loader)


def create_embeddings(encoder, full_loader, device):
    """
    对全量数据集生成图片嵌入表达（编码器推理）

    Returns:
        嵌入矩阵 (N, embedding_dim) 的 ndarray
    """
    encoder.eval()
    embeddings = torch.empty(0)

    with torch.no_grad():
        for inputs, _ in full_loader:
            inputs = inputs.to(device)
            # 编码器前向传播
            output = encoder(inputs).cpu()
            # 拼接到嵌入张量中
            embeddings = torch.cat((embeddings, output), dim=0)

    # 将嵌入张量转换为二维嵌入矩阵
    embeddings = embeddings.reshape(embeddings.shape[0], -1).numpy()

    return embeddings


def compute_similar_images(encoder, image_tensor, num_images, embeddings, device):
    """
    计算相似图片

    Args:
        encoder: 编码器模型
        image_tensor: 输入图像张量
        num_images: 返回的相似图片数量
        embeddings: 嵌入矩阵
        device: 设备

    Returns:
        最相似的 K 个图片索引列表
    """
    # 将图像移动至设备
    image_tensor = image_tensor.to(device)

    # 前向传播，得到输入图像的嵌入表达
    with torch.no_grad():
        image_embedding = encoder(image_tensor).cpu().numpy()

    # 转为二维结构
    image_vector = image_embedding.reshape((image_embedding.shape[0], -1))

    # 定义 KNN 模型
    knn = NearestNeighbors(n_neighbors=num_images, metric='cosine')

    # 在嵌入矩阵上拟合
    knn.fit(embeddings)

    # 查询 k 近邻
    _, indices = knn.kneighbors(image_vector)

    return indices.tolist()
