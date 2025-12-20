# Storage 目录

此目录用于存储训练好的模型、数据集和标签文件。

## 目录结构

```
storage/
└── image-processing/
    ├── checkpoint/        # 训练好的模型权重文件
    │   ├── classifier.pt  # 分类模型
    │   ├── denoiser.pt    # 去噪模型
    │   ├── encoder.pt     # 编码器模型
    │   ├── decoder.pt     # 解码器模型
    │   └── embeddings.npy # 图像嵌入向量
    │
    ├── dataset/           # 数据集文件
    │   └── *.jpg
    │
    ├── labels/            # 标签文件
    │   └── fashion-labels.csv
    │
    └── runs/              # TensorBoard 日志文件
        └── *.tfevents
```

## 说明

- `checkpoint/` - 存放训练完成的模型权重文件
- `dataset/` - 存放训练和测试用的图像数据集
- `labels/` - 存放数据集的标签文件
- `runs/` - 存放 TensorBoard 训练日志

## 注意

- 此目录内容已加入 .gitignore，仅保留目录结构
- 模型和数据集需要单独下载或训练生成
