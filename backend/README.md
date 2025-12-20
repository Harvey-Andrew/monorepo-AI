# Backend

基于 FastAPI 的 AI 推理后端服务。

## 目录结构

```
backend/
├── app.py              # FastAPI 主入口
├── requirements.txt    # 基础依赖
├── core/               # 核心模块
│   ├── config.py       # 配置管理
│   ├── model_loader.py # 模型加载器
│   └── protocol.py     # Pydantic 协议
├── storage/            # 模型和数据集存储
└── apps/               # AI 应用模块
    ├── denoising/      # 图像去噪
    ├── classification/ # 图像分类
    └── similarity/     # 相似检索
```

## 安装依赖

### 1. 创建虚拟环境

```bash
cd backend
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 2. 安装基础依赖

```bash
pip install -r requirements.txt
```

### 3. 安装 Image Processing 模块依赖

**CPU 版本：**

```bash
pip install -r apps/image_processing/requirements.txt
```

**GPU 版本（CUDA 12.1）：**

```bash
pip install -r apps/image_processing/requirements.txt --extra-index-url https://download.pytorch.org/whl/cu121
```

> **注意**: GPU 版本需要安装对应版本的 CUDA Toolkit。如果使用其他 CUDA 版本，请修改 `cu121` 为对应版本号（如 `cu118` 对应 CUDA 11.8）。

## 启动服务

```bash
python app.py
```
