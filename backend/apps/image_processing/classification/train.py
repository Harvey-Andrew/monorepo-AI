"""
图像分类 - 模型训练脚本

使用方法:
    cd backend/apps/image-processing/classification
    python train.py
"""

import torch
from torch import nn, optim
from torch.utils.data import DataLoader
from tqdm import tqdm

from config import (
    SEED,
    TRAIN_BATCH_SIZE,
    VAL_BATCH_SIZE,
    LEARNING_RATE,
    EPOCHS,
    CLASSIFIER_MODEL_PATH,
    RUNS_DIR,
)
from data import create_dataset
from model import Classifier
from engine import train_epoch, test_epoch


def seed_everything(seed: int):
    """设置随机种子"""
    import random
    import numpy as np

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def main():
    """训练主流程"""
    # 设备检测
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"使用设备: {device}")

    # 设置随机种子
    seed_everything(SEED)

    # 1. 创建数据集
    print("正在创建数据集...")
    train_dataset, val_dataset = create_dataset()
    print(f"训练集: {len(train_dataset)} | 验证集: {len(val_dataset)}")
    print("============= 1. 数据集创建完成 =============")

    # 2. 定义数据加载器
    train_loader = DataLoader(
        train_dataset, TRAIN_BATCH_SIZE, shuffle=True, drop_last=True
    )
    val_loader = DataLoader(val_dataset, VAL_BATCH_SIZE, shuffle=False)
    print("============= 2. 数据加载器创建完成 =============")

    # 3. 定义模型、损失函数和优化器
    model = Classifier()
    model.to(device)
    loss_fn = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=LEARNING_RATE)
    print("============= 3. 模型创建完成 =============")

    # TensorBoard
    try:
        from torch.utils.tensorboard import SummaryWriter

        RUNS_DIR.mkdir(parents=True, exist_ok=True)
        writer = SummaryWriter(str(RUNS_DIR))
        use_tensorboard = True
    except ImportError:
        print("警告: TensorBoard 未安装，跳过日志记录")
        writer = None
        use_tensorboard = False

    # 4. 训练模型
    min_val_loss = float("inf")

    for epoch in tqdm(range(EPOCHS), desc="训练进度"):
        # 训练一轮
        train_loss = train_epoch(model, train_loader, loss_fn, optimizer, device)
        print(f"\nEpoch {epoch + 1}/{EPOCHS}, Train Loss: {train_loss:.6f}")

        # 验证
        val_loss, val_acc = test_epoch(model, val_loader, loss_fn, device)
        print(
            f"Epoch {epoch + 1}/{EPOCHS}, Val Loss: {val_loss:.6f}, Val Acc: {val_acc:.4f}"
        )

        # 记录到 TensorBoard
        if use_tensorboard:
            writer.add_scalar("Loss/train", train_loss, epoch)
            writer.add_scalar("Loss/val", val_loss, epoch)
            writer.add_scalar("Accuracy/val", val_acc, epoch)

        # 保存最佳模型
        if val_loss < min_val_loss:
            print("验证损失减小，保存模型...")
            CLASSIFIER_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
            torch.save(model.state_dict(), str(CLASSIFIER_MODEL_PATH))
            min_val_loss = val_loss
        else:
            print("验证损失没有减小，不保存模型。")

    if use_tensorboard:
        writer.close()

    print("============= 4. 模型训练完成 =============")
    print(f"最终验证损失: {min_val_loss:.6f}")
    print(f"模型已保存至: {CLASSIFIER_MODEL_PATH}")


if __name__ == "__main__":
    main()
