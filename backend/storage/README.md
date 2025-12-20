# Storage 目录

此目录用于存储训练好的模型和数据集。

## 目录结构

```
storage/
└── image-processing/
    ├── checkpoint/    # 训练好的模型权重文件
    │   └── *.pt
    │
    └── dataset/       # 数据集文件
        └── *.jpg
    │
    └── runs/          # TensorBoard 日志文件
        └── *.tfevents
```

## 说明

- `checkpoint/` - 存放训练完成的模型权重文件（.pt）
- `dataset/` - 存放训练和测试用的数据集

## 注意

- 此目录内容已加入 .gitignore，仅保留目录结构
- 模型和数据集需要单独下载或训练生成
