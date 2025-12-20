"""
图像去噪 - 训练/测试引擎
"""

__all__ = ["train_epoch", "test_epoch"]

import torch


def train_epoch(model, train_loader, loss_fn, optimizer, device):
    """
    执行一轮训练

    Returns:
        平均训练损失
    """
    model.train()
    total_loss = 0

    for inputs, targets in train_loader:
        inputs, targets = inputs.to(device), targets.to(device)

        # 前向传播
        outputs = model(inputs)
        loss = loss_fn(outputs, targets)

        # 反向传播
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    return total_loss / len(train_loader)


def test_epoch(model, test_loader, loss_fn, device):
    """
    执行一次验证/测试

    Returns:
        平均损失
    """
    model.eval()
    total_loss = 0

    with torch.no_grad():
        for inputs, targets in test_loader:
            inputs, targets = inputs.to(device), targets.to(device)

            # 前向传播
            outputs = model(inputs)
            loss = loss_fn(outputs, targets)

            # 累计损失
            total_loss += loss.item()

    return total_loss / len(test_loader)
