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
│   ├── components/           # UI 组件库
│   ├── composables/          # 业务逻辑 (含防抖处理)
│   ├── utils/                # 通用工具 (含 Axios 拦截器)
│   └── plugins/              # Nuxt 插件 (Element Plus)
│
├── backend/                  # FastAPI 后端服务
│   ├── apps/                 # 核心算法模块 (去噪/分类/相似度)
│   ├── storage/              # 模型权重与数据集存储
│   ├── common/               # 共享模式与限流配置
│   └── app.py                # 主程序入口
│
├── docs/                     # 项目文档与截图
└── package.json              # Monorepo 根配置
```

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

可在 `frontend/.env` 配置后端接口地址：

```env
PYTHON_API_BASE=http://127.0.0.1:9000
```

## 🔧 技术栈详情

### 前端

- **框架**: Nuxt 3 (Vue 3, TypeScript)
- **UI**: Element Plus
- **工具**: @vueuse/core, Axios
- **请求**: 统一拦截错误并调用 `ElMessage` 提示

### 后端

- **框架**: FastAPI (Python)
- **AI**: PyTorch, Torchvision
- **保护**: slowapi (限流限制: 10次/分钟/IP)

## 📊 模型训练

训练模型时会自动记录日志到后端 `runs/` 目录。可使用 TensorBoard 查看曲线：

```bash
cd backend
tensorboard --logdir=runs
```

## 📄 开源协议

[MIT License](LICENSE)
