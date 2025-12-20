"""
图像相似度模型

卷积编码器/解码器
"""

import torch
import torch.nn as nn

__all__ = ["ConvEncoder", "ConvDecoder"]


class ConvEncoder(nn.Module):
    """卷积编码器"""

    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.conv4 = nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1)
        self.conv5 = nn.Conv2d(128, 256, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(2, stride=2)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = torch.relu(self.conv1(x))
        x = self.pool(x)
        x = torch.relu(self.conv2(x))
        x = self.pool(x)
        x = torch.relu(self.conv3(x))
        x = self.pool(x)
        x = torch.relu(self.conv4(x))
        x = self.pool(x)
        x = torch.relu(self.conv5(x))
        x = self.pool(x)
        return x


class ConvDecoder(nn.Module):
    """卷积解码器"""

    def __init__(self):
        super().__init__()
        self.conv_t1 = nn.ConvTranspose2d(256, 128, kernel_size=2, stride=2)
        self.conv_t2 = nn.ConvTranspose2d(128, 64, kernel_size=2, stride=2)
        self.conv_t3 = nn.ConvTranspose2d(64, 32, kernel_size=2, stride=2)
        self.conv_t4 = nn.ConvTranspose2d(32, 16, kernel_size=2, stride=2)
        self.conv_t5 = nn.ConvTranspose2d(16, 3, kernel_size=2, stride=2)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = torch.relu(self.conv_t1(x))
        x = torch.relu(self.conv_t2(x))
        x = torch.relu(self.conv_t3(x))
        x = torch.relu(self.conv_t4(x))
        x = torch.sigmoid(self.conv_t5(x))
        return x
