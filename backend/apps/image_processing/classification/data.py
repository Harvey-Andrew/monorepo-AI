"""
图像分类 - 数据集
"""

__all__ = ["create_dataset", "ImageLabelDataset"]

import os
import re

import pandas as pd
import torchvision.transforms as T
from PIL import Image
from torch.utils.data import Dataset, random_split

try:
    from .config import FASHION_LABELS_PATH, IMG_PATH, IMG_SIZE, TEST_RATIO, TRAIN_RATIO
except ImportError:
    from config import FASHION_LABELS_PATH, IMG_PATH, IMG_SIZE, TEST_RATIO, TRAIN_RATIO


def sorted_alphanum(file_list):
    """自然排序文件列表"""

    def convert(text):
        return int(text) if text.isdigit() else text.lower()

    def alphanum_key(key):
        return [convert(c) for c in re.split("([0-9]+)", key)]

    return sorted(file_list, key=alphanum_key)


class ImageLabelDataset(Dataset):
    """带标签的图像数据集"""

    def __init__(self, main_dir, label_path, transform=None):
        self.main_dir = main_dir
        self.transform = transform
        self.imgs = sorted_alphanum(os.listdir(main_dir))
        # 读取分类标签
        labels = pd.read_csv(label_path)
        self.labels_dict = dict(zip(labels["id"], labels["target"], strict=False))

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
        # 获取标签
        img_label = self.labels_dict[idx]

        return tensor_image, img_label


def create_dataset(img_path=None, label_path=None):
    """
    创建训练和验证数据集

    Returns:
        (train_dataset, val_dataset)
    """
    img_path = img_path or str(IMG_PATH)
    label_path = label_path or str(FASHION_LABELS_PATH)

    # 定义图像预处理
    transform = T.Compose([T.Resize(IMG_SIZE), T.ToTensor()])

    # 创建完整数据集
    dataset = ImageLabelDataset(img_path, label_path, transform)

    # 切分数据集
    train_dataset, val_dataset = random_split(dataset, [TRAIN_RATIO, TEST_RATIO])

    return train_dataset, val_dataset


if __name__ == "__main__":
    train_dataset, val_dataset = create_dataset()
    print(f"训练集大小: {len(train_dataset)}")
    print(f"验证集大小: {len(val_dataset)}")
