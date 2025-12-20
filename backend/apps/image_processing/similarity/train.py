"""
相似检索 - 模型训练脚本

使用方法:
    cd backend/apps/image-processing/similarity
    python train.py
"""

import numpy as np
import torch
from torch import nn, optim
from torch.utils.data import DataLoader
from tqdm import tqdm

from config import (
    SEED,
    TRAIN_BATCH_SIZE,
    VAL_BATCH_SIZE,
    FULL_BATCH_SIZE,
    LEARNING_RATE,
    EPOCHS,
    ENCODER_MODEL_PATH,
    DECODER_MODEL_PATH,
    EMBEDDING_PATH,
    RUNS_DIR,
)
from data import create_dataset
from model import ConvEncoder, ConvDecoder
from engine import train_epoch, test_epoch, create_embeddings


def seed_everything(seed: int):
    """设置随机种子"""
    import random

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
    dataset, train_dataset, val_dataset = create_dataset()
    print(f"完整数据集: {len(dataset)} | 训练集: {len(train_dataset)} | 验证集: {len(val_dataset)}")
    print("============= 1. 数据集创建完成 =============")

    # 2. 定义数据加载器
    train_loader = DataLoader(
        train_dataset, TRAIN_BATCH_SIZE, shuffle=True, drop_last=True
    )
    val_loader = DataLoader(val_dataset, VAL_BATCH_SIZE, shuffle=False)
    full_loader = DataLoader(dataset, FULL_BATCH_SIZE, shuffle=False)
    print("============= 2. 数据加载器创建完成 =============")

    # 3. 定义模型、损失函数和优化器
    encoder = ConvEncoder()
    decoder = ConvDecoder()
    encoder.to(device)
    decoder.to(device)
    
    loss_fn = nn.MSELoss()  # 均方误差损失
    params = list(encoder.parameters()) + list(decoder.parameters())
    optimizer = optim.AdamW(params, lr=LEARNING_RATE)
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
        train_loss = train_epoch(encoder, decoder, train_loader, loss_fn, optimizer, device)
        print(f"\nEpoch {epoch + 1}/{EPOCHS}, Train Loss: {train_loss:.6f}")

        # 验证
        val_loss = test_epoch(encoder, decoder, val_loader, loss_fn, device)
        print(f"Epoch {epoch + 1}/{EPOCHS}, Val Loss: {val_loss:.6f}")

        # 记录到 TensorBoard
        if use_tensorboard:
            writer.add_scalar("Loss/train", train_loss, epoch)
            writer.add_scalar("Loss/val", val_loss, epoch)

        # 保存最佳模型
        if val_loss < min_val_loss:
            print("验证损失减小，保存模型...")
            ENCODER_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
            torch.save(encoder.state_dict(), str(ENCODER_MODEL_PATH))
            torch.save(decoder.state_dict(), str(DECODER_MODEL_PATH))
            min_val_loss = val_loss
        else:
            print("验证损失没有减小，不保存模型。")

    if use_tensorboard:
        writer.close()

    print("============= 4. 模型训练完成 =============")
    print(f"最终验证损失: {min_val_loss:.6f}")

    # 5. 生成图像嵌入矩阵
    print("正在生成嵌入矩阵...")
    
    # 加载最优模型
    encoder.load_state_dict(torch.load(str(ENCODER_MODEL_PATH)))
    
    # 生成嵌入矩阵
    embeddings = create_embeddings(encoder, full_loader, device)
    
    # 保存嵌入矩阵
    EMBEDDING_PATH.parent.mkdir(parents=True, exist_ok=True)
    np.save(str(EMBEDDING_PATH), embeddings)
    
    print(f"嵌入矩阵形状: {embeddings.shape}")
    print(f"嵌入矩阵已保存至: {EMBEDDING_PATH}")
    print("============= 5. 嵌入矩阵生成完成 =============")


if __name__ == "__main__":
    main()
