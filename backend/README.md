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

## 启动服务

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
