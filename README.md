# My Local AI Hub 🧠

> **本地 AI 推理中心** — 基于 `Nuxt 3 + FastAPI + PyTorch` 的全栈 AI 平台

集成 **5 大 AI 模块**，涵盖计算机视觉、自然语言处理与大模型对话，采用 `pnpm workspace` Monorepo 架构，一套服务、一键启动。

## ✨ 核心特性

- 🧩 **5 合 1 AI 平台**: 图像处理 · 智能聊天 · 商品分类 · 新闻分析 · 地址对齐
- ⚡ **全栈响应式**: Nuxt 3 SSR + FastAPI 异步接口，极速体验
- 🛡️ **生产级防护**: 后端限流 (slowapi) + 前端防抖 (VueUse) + Axios 全局错误拦截
- 🔧 **工程化完备**: Husky + lint-staged 提交检查 · ESLint + Prettier + Ruff 代码规范 · 一键安装脚本
- 🚀 **GPU 加速**: 自动检测 CUDA，支持 GPU/CPU 双模式推理

---

## 🏗️ 项目结构

```
monorepo-AI/
├── frontend/                    # Nuxt 3 前端应用
│   ├── pages/apps/              # 功能页面路由
│   │   ├── image-processing/    #   图像处理 (去噪/分类/相似检索)
│   │   ├── chat/                #   AI 聊天助手
│   │   ├── product-classification/ # 商品标题分类
│   │   ├── ai-news/             #   AI 新闻分析
│   │   └── address-alignment/   #   地址对齐
│   ├── components/              # UI 组件库
│   ├── composables/             # 业务逻辑组合式函数
│   ├── utils/                   # 通用工具 (Axios 拦截器)
│   └── plugins/                 # Nuxt 插件
│
├── backend/                     # FastAPI 后端服务
│   ├── app.py                   # 主程序入口
│   ├── core/                    # 核心模块 (配置/模型加载/协议)
│   ├── common/                  # 共享模块 (限流/通用 Schema)
│   └── apps/                    # AI 应用模块
│       ├── image_processing/    #   图像去噪 + 分类 + 相似检索
│       ├── chat/                #   AI 聊天 (Gemini API)
│       ├── product_classification/ # 商品标题分类 (BERT)
│       ├── ai_news/             #   新闻分类 + 自动摘要
│       └── address_alignment/   #   地址序列标注 (NER)
│
├── product_classification/      # 商品分类模型训练代码
├── scripts/                     # 工具脚本 (类型生成等)
├── eslint.config.mjs            # ESLint 配置
├── ruff.toml                    # Ruff 配置
└── package.json                 # Monorepo 根配置
```

---

## 🧩 功能模块

### 🖼️ 图像处理

基于 CNN / ResNet 的深度学习图像处理。

| 功能     | 说明                          | API                        |
| -------- | ----------------------------- | -------------------------- |
| 图像去噪 | 自动去除图像噪点              | `POST /api/denoising`      |
| 商品分类 | ResNet 改进模型，识别商品类别 | `POST /api/classification` |
| 相似检索 | 特征嵌入 + 余弦相似度，毫秒级 | `POST /api/simimages`      |

**前端页面**: `http://localhost:3000/apps/image-processing`

---

### 🤖 AI 聊天助手

基于 **Google Gemini API** 的智能对话系统。

| 功能       | 说明                    |
| ---------- | ----------------------- |
| 流式对话   | SSE 实时推送，逐字显示  |
| 多会话管理 | 创建、切换、删除会话    |
| 本地持久化 | 自动保存到 localStorage |
| 中文优化   | 默认中文系统提示词      |

**前端页面**: `http://localhost:3000/apps/chat`

| API 端点               | 说明                    |
| ---------------------- | ----------------------- |
| `POST /api/chat`       | 聊天接口（流式/非流式） |
| `GET /api/chat/health` | 服务健康检查            |

---

### 📦 商品标题分类

基于 **BERT** 预训练模型的商品文本分类，输入商品标题自动识别类别。

| 功能     | 说明                 |
| -------- | -------------------- |
| 单条预测 | 输入标题返回分类结果 |
| 批量预测 | 支持批量标题一次分类 |

| API 端点                                         | 说明     |
| ------------------------------------------------ | -------- |
| `POST /api/product-classification/predict`       | 单条分类 |
| `POST /api/product-classification/predict/batch` | 批量分类 |

**前端页面**: `http://localhost:3000/apps/product-classification`

---

### 📰 AI 新闻分析

基于 Transformer 的新闻文本分析系统，支持分类、摘要和综合分析。

| 功能     | 说明                                           |
| -------- | ---------------------------------------------- |
| 新闻分类 | 7 类：财经、社会、教育、科技、时政、体育、游戏 |
| 自动摘要 | 基于 Seq2Seq 模型生成摘要                      |
| 综合分析 | 同时返回分类结果和摘要                         |

| API 端点                      | 说明     |
| ----------------------------- | -------- |
| `POST /api/ai-news/classify`  | 新闻分类 |
| `POST /api/ai-news/summarize` | 自动摘要 |
| `POST /api/ai-news/analyze`   | 综合分析 |
| `GET /api/ai-news/status`     | 模型状态 |

**前端页面**: `http://localhost:3000/apps/ai-news`

---

### 📍 地址对齐

基于 **NER 序列标注**的地址结构化提取，将非标准地址解析为省/市/区/街道等字段。

| 功能     | 说明                       |
| -------- | -------------------------- |
| 地址对齐 | 结构化提取 + 数据库校验    |
| 地址提取 | 纯模型提取（无数据库校验） |
| 序列标注 | 返回每个字符的 BIO 标签    |

| API 端点                              | 说明     |
| ------------------------------------- | -------- |
| `POST /api/address-alignment/align`   | 地址对齐 |
| `POST /api/address-alignment/extract` | 地址提取 |
| `POST /api/address-alignment/tagging` | 序列标注 |
| `GET /api/address-alignment/status`   | 模型状态 |

**前端页面**: `http://localhost:3000/apps/address-alignment`

---

## 🚀 快速开始

### 1. 环境准备

| 依赖    | 版本要求  | 说明         |
| ------- | --------- | ------------ |
| Node.js | >= 18.0.0 | 推荐 v20+    |
| pnpm    | >= 8.0.0  | 包管理器     |
| Python  | >= 3.10   | 推荐 3.12    |
| CUDA    | 可选      | GPU 加速推理 |

### 2. 一键安装（推荐）

```bash
# Windows 用户：双击运行一键安装脚本
install_dependencies.bat
```

脚本会自动创建 Conda 环境、安装前后端依赖、配置 PyTorch（支持选择 CUDA 版本）。

### 3. 手动安装

```bash
# 安装前端 + 根依赖
pnpm install

# 安装 Python 依赖
pip install -r backend/requirements.txt
```

### 4. 下载资源

> 📦 **商品图片数据集**和**预计算嵌入向量**（相似推荐功能必需）
>
> - **下载链接**：[百度网盘](https://pan.baidu.com/s/1O-gOuko7DuRDR7hn6jfutw?pwd=9qd7) | **提取码**：`9qd7`
> - **数据集**：将 `dataset.zip` 解压到 `backend/storage/image-processing/dataset/`
> - **模型权重**：将 `.pt` 文件和 `embeddings.npy` 放到 `backend/storage/image-processing/checkpoint/`

### 5. 启动开发服务器

```bash
# 同时启动前端 (:3000) 和后端 (:9000)
pnpm dev

# 或分别启动
pnpm dev:client    # 仅前端
pnpm dev:server    # 仅后端
```

启动后访问：

- 🌐 **前端**: http://localhost:3000
- 📡 **后端 API**: http://127.0.0.1:9000
- 📖 **API 文档**: http://127.0.0.1:9000/docs

---

## ⚙️ 环境变量

### 前端

在 `frontend/.env` 配置后端接口地址：

```env
PYTHON_API_BASE=http://127.0.0.1:9000
```

### 后端

AI 聊天功能需要配置 Google API Key：

```powershell
# Windows PowerShell
$env:GOOGLE_API_KEY = "your_api_key_here"
```

```bash
# Linux/macOS
export GOOGLE_API_KEY="your_api_key_here"
```

> 💡 获取 API Key：访问 [Google AI Studio](https://aistudio.google.com/apikey) 创建密钥

---

## 🔧 技术栈

### 前端

| 技术           | 说明                 |
| -------------- | -------------------- |
| Nuxt 3         | Vue 3 + TypeScript   |
| Element Plus   | UI 组件库            |
| Element Plus X | AI 对话组件          |
| @vueuse/core   | 组合式工具函数       |
| Axios          | HTTP 请求 + 全局拦截 |
| SCSS           | 样式预处理           |

### 后端

| 技术         | 说明                       |
| ------------ | -------------------------- |
| FastAPI      | 异步 Web 框架              |
| PyTorch      | 深度学习推理               |
| Transformers | BERT / Seq2Seq 预训练模型  |
| google-genai | Gemini 大模型 API          |
| slowapi      | 接口限流 (10-30次/分钟/IP) |
| RapidFuzz    | 模糊匹配 (地址对齐)        |

### 工程化

| 工具                | 说明                    |
| ------------------- | ----------------------- |
| pnpm workspace      | Monorepo 管理           |
| Husky + lint-staged | Git 提交前自动检查      |
| ESLint + Prettier   | 前端代码检查与格式化    |
| Ruff                | Python 代码检查与格式化 |

---

## 📊 模型训练

训练模型时自动记录日志到 `backend/runs/`，可使用 TensorBoard 查看训练曲线：

```bash
cd backend
tensorboard --logdir=runs
```

---

## 📝 代码规范

### 前端 (ESLint + Prettier)

```bash
pnpm lint          # 检查代码
pnpm lint:fix      # 自动修复
pnpm format        # 格式化
```

### 后端 (Ruff)

```bash
pnpm lint:py       # 检查代码
pnpm lint:py:fix   # 自动修复
pnpm format:py     # 格式化
```

### 全量格式化

```bash
pnpm format:all    # 前后端一起格式化
```

**Ruff 启用的规则集**：

| 规则  | 说明                  |
| ----- | --------------------- |
| `E/W` | pycodestyle 错误/警告 |
| `F`   | Pyflakes              |
| `I`   | isort 导入排序        |
| `B`   | flake8-bugbear        |
| `C4`  | flake8-comprehensions |
| `UP`  | pyupgrade             |

---

## 📂 常用脚本

| 命令               | 说明                     |
| ------------------ | ------------------------ |
| `pnpm dev`         | 启动全栈开发服务器       |
| `pnpm build`       | 构建前端生产包           |
| `pnpm install:all` | 安装全部依赖 (前端+后端) |
| `pnpm gen:types`   | 生成前后端共享类型       |
| `pnpm format:all`  | 全量代码格式化           |

---

## 📄 开源协议

[MIT License](LICENSE)
