"""
图像去噪 - 数据集
"""

__all__ = ["create_dataset", "ImageDataset"]

import os
import re

import torch
import torchvision.transforms as T
from PIL import Image
from torch.utils.data import Dataset, random_split

from .config import IMG_PATH, IMG_SIZE, NOISE_RATIO, TEST_RATIO, TRAIN_RATIO


def sorted_alphanum(file_list):
    """自然排序文件列表"""

    def convert(text):
        return int(text) if text.isdigit() else text.lower()

    def alphanum_key(key):
        return [convert(c) for c in re.split("([0-9]+)", key)]

    return sorted(file_list, key=alphanum_key)


class ImageDataset(Dataset):
    """图像数据集（用于去噪任务）"""

    def __init__(self, main_dir, transform=None):
        self.main_dir = main_dir
        self.transform = transform
        self.imgs = sorted_alphanum(os.listdir(main_dir))

    def __len__(self):
        return len(self.imgs)

    def __getitem__(self, idx):
        # 获取图片路径
        img_path = os.path.join(self.main_dir, self.imgs[idx])
        # 加载图像
        image = Image.open(img_path).convert("RGB")
        # 预处理
        if self.transform is not None:
            tensor_image = self.transform(image)
        else:
            raise ValueError("transform 参数不能为 None！")

        # 基于原图加入噪声，构建输入数据
        noisy_image = tensor_image + torch.randn_like(tensor_image) * NOISE_RATIO
        # 将噪声图像数据裁剪到[0, 1]范围内
        noisy_image = torch.clamp(noisy_image, 0.0, 1.0)

        return noisy_image, tensor_image  # 返回 (噪声图像, 原图像)


def create_dataset(img_path=None):
    """
    创建训练和验证数据集

    Returns:
        (train_dataset, val_dataset)
    """
    img_path = img_path or str(IMG_PATH)

    # 定义图像预处理
    transform = T.Compose([T.Resize(IMG_SIZE), T.ToTensor()])

    # 创建完整数据集
    dataset = ImageDataset(img_path, transform)

    # 切分数据集
    train_dataset, val_dataset = random_split(dataset, [TRAIN_RATIO, TEST_RATIO])

    return train_dataset, val_dataset


if __name__ == "__main__":
    train_dataset, val_dataset = create_dataset()
    print(f"训练集大小: {len(train_dataset)}")
    print(f"验证集大小: {len(val_dataset)}")
