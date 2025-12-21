# 智图寻宝 - AI 驱动的商品识别系统 (Monorepo)

基于 **Nuxt 3 + FastAPI + PyTorch** 的高性能智能商品识别系统。采用 `pnpm workspace` 管理的 Monorepo 结构，集成深度学习模型实现图像去噪、商品分类及相似商品检索。

## 📸 效果预览

|               首页界面               |               功能演示               |
| :----------------------------------: | :----------------------------------: |
| ![首页](./docs/screenshots/home.png) | ![演示](./docs/screenshots/demo.png) |

## ✨ 核心特性

- ⚡ **全栈响应式**: 基于 Nuxt 3 和 FastAPI 的现代化架构，响应极速。
- 🛡️ **安全与稳定**:
  - **后端限流 (Rate Limiting)**: 集成 `slowapi`，防止接口滥用，提供友好中文提示。
  - **前端防抖 (Debounce)**: 使用 `VueUse` 进行按钮点击防抖，减少无效请求。
  - **统一错误处理**: Axios 拦截器全局接管错误提示，提升开发效率与体验。
- 🖼️ **AI 图像处理**:
  - **自适应去噪**: 基于深度学习的模型处理噪声图片。
  - **智能分类**: 自动识别商品所属类别。
  - **相似检索**: 毫秒级检索海量商品库中的相似图片。

## 🏗️ 项目结构

```
monorepo-image-processing/
├── frontend/                 # Nuxt 3 前端应用
│   ├── pages/                # 页面路由
│   │   └── apps/             # 功能页面 (chat.vue, denoising.vue, ...)
│   ├── components/           # UI 组件库
│   ├── composables/          # 业务逻辑 (useChat, useImageProcess)
│   ├── utils/                # 通用工具 (含 Axios 拦截器)
│   └── plugins/              # Nuxt 插件 (Element Plus)
│
├── backend/                  # FastAPI 后端服务
│   ├── apps/
│   │   ├── chat/             # AI 聊天模块 (Gemini API)
│   │   └── image_processing/ # 图像处理模块
│   │       ├── denoising/    # 图像去噪
│   │       ├── classification/ # 商品分类
│   │       └── similarity/   # 相似检索
│   ├── storage/              # 模型权重与数据集存储
│   ├── common/               # 共享模式与限流配置
│   └── app.py                # 主程序入口
│
├── docs/                     # 项目文档与截图
└── package.json              # Monorepo 根配置
```

---

## 🧩 功能模块

### 🤖 AI 聊天助手

基于 **Google Gemini API** 的智能对话系统，支持流式响应。

| 功能       | 说明                          |
| ---------- | ----------------------------- |
| 流式对话   | SSE 实时推送，AI 回复逐字显示 |
| 多会话管理 | 创建、切换、删除会话          |
| 本地持久化 | 会话自动保存到 localStorage   |
| 中文优化   | 默认中文系统提示词            |

**访问地址**: `http://localhost:3000/apps/chat`

**API 端点**:

- `POST /api/chat` - 聊天接口（支持流式/非流式）
- `GET /api/chat/health` - 健康检查

---

### 🖼️ 图像处理

#### 1. 图像去噪 (Denoising)

使用深度学习模型自动去除图像噪点，提升图片质量。

| 项目 | 说明                        |
| ---- | --------------------------- |
| 模型 | 基于 CNN 的去噪网络         |
| 输入 | 任意尺寸图片 (JPG/PNG/WebP) |
| 输出 | 加噪图 + 去噪结果 (Base64)  |

**API**: `POST /api/denoising`

---

#### 2. 商品分类 (Classification)

智能识别商品类别，基于自训练分类模型。

| 项目 | 说明             |
| ---- | ---------------- |
| 模型 | ResNet 改进模型  |
| 类别 | 支持多种商品类别 |
| 输出 | 分类标签         |

**API**: `POST /api/classification`

---

#### 3. 相似检索 (Similarity)

毫秒级检索海量商品库中的相似图片。

| 项目 | 说明                  |
| ---- | --------------------- |
| 算法 | 特征嵌入 + 余弦相似度 |
| 速度 | 毫秒级响应            |
| 输出 | Top-K 相似图片 URL    |

**API**: `POST /api/simimages`

---

## 🚀 快速开始

### 1. 环境准备

- **Node.js**: >= 18.0.0 (推荐 v20+)
- **pnpm**: >= 8.0.0
- **Python**: >= 3.10
- **CUDA**: 可选（用于 GPU 加速推断）

### 2. 下载资源

> 📦 **商品图片数据集**和**预计算嵌入向量**（相似推荐功能必需）
>
> - **下载链接**：[百度网盘](https://pan.baidu.com/s/1O-gOuko7DuRDR7hn6jfutw?pwd=9qd7)
> - **提取码**：`9qd7 `
> - **数据集位置**：将 `dataset.zip` 解压到 `backend/storage/image-processing/dataset/`
> - **权重位置**：将模型权重（`.pt`）和 `embeddings.npy` 放到 `backend/storage/image-processing/checkpoint/`

### 3. 安装与运行

```bash
# 安装根依赖
pnpm install

# 启动开发服务器 (同时启动前端:3000 和 后端:9000)
pnpm dev
```

## ⚙️ 环境变量

### 前端配置

可在 `frontend/.env` 配置后端接口地址：

```env
PYTHON_API_BASE=http://127.0.0.1:9000
```

### 后端配置

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

## 🔧 技术栈详情

### 前端

- **框架**: Nuxt 3 (Vue 3, TypeScript)
- **UI**: Element Plus, Element Plus X (AI组件库)
- **工具**: @vueuse/core, Axios
- **请求**: 统一拦截错误并调用 `ElMessage` 提示

### 后端

- **框架**: FastAPI (Python)
- **AI**: PyTorch, Torchvision, google-genai
- **保护**: slowapi (限流限制: 10次/分钟/IP)

## 📊 模型训练

训练模型时会自动记录日志到后端 `runs/` 目录。可使用 TensorBoard 查看曲线：

```bash
cd backend
tensorboard --logdir=runs
```

## � 代码规范

本项目使用统一的代码规范工具确保代码质量。

### 前端 (ESLint + Prettier)

```bash
# 检查代码
npx eslint frontend

# 自动修复
npx eslint frontend --fix

# 格式化代码
npx prettier --write frontend
```

**配置文件**：

- `eslint.config.mjs` - ESLint 规则配置
- `.prettierrc` - Prettier 格式化配置

### 后端 (Ruff)

```bash
# 检查代码
ruff check backend

# 自动修复
ruff check backend --fix

# 格式化代码
ruff format backend
```

**配置文件**：`ruff.toml`

**启用的规则集**：
| 规则 | 说明 |
|------|------|
| `E/W` | pycodestyle 错误/警告 |
| `F` | Pyflakes |
| `I` | isort 导入排序 |
| `B` | flake8-bugbear |
| `C4` | flake8-comprehensions |
| `UP` | pyupgrade |

## �📄 开源协议

[MIT License](LICENSE)
