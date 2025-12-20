# API 接口规范

本文档定义了智图寻宝项目的统一接口规范，确保前后端类型安全、命名一致、易于维护。

---

## 1. 基础规范

### 1.1 URL 路径规范

| 规则         | 说明                   | 示例                                           |
| ------------ | ---------------------- | ---------------------------------------------- |
| 使用小写     | 路径全部小写           | `/api/denoising`                               |
| 使用连字符   | 多词路径使用连字符     | `/api/similar-images`                          |
| 资源名用名词 | 表示资源而非动作       | `/api/classification`（✓）`/api/classify`（✗） |
| API 前缀     | 所有接口以 `/api` 开头 | `/api/denoising`                               |

### 1.2 HTTP 方法规范

| 方法     | 用途          | 示例                   |
| -------- | ------------- | ---------------------- |
| `GET`    | 查询资源      | `GET /api/health`      |
| `POST`   | 创建/处理资源 | `POST /api/denoising`  |
| `PUT`    | 全量更新      | `PUT /api/models/{id}` |
| `PATCH`  | 部分更新      | `PATCH /api/settings`  |
| `DELETE` | 删除资源      | `DELETE /api/cache`    |

### 1.3 通用响应结构

所有 API 响应应遵循统一的包装格式 `Result<T>`：

```typescript
/**
 * 业务状态码枚举（建议由后端统一维护并同步给前端）
 */
export enum ApiCode {
  SUCCESS = 200,
  BAD_REQUEST = 400,
  UNAUTHORIZED = 401,
  FORBIDDEN = 403,
  NOT_FOUND = 404,
  VALIDATION_ERROR = 1001, // 字段校验失败
  BUSINESS_ERROR = 2000, // 通用业务逻辑错误
  SERVER_ERROR = 500, // 服务器内部错误
}

/**
 * 统一接口返回规范
 */
export interface Result<T = any> {
  code: ApiCode | number; // 业务状态码
  data: T; // 成功时为数据，失败时通常为 null
  message: string; // 提示信息（建议必填，方便前端直接展示）
}

/**
 * 分页数据标准格式
 */
export interface PageResult<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}
```

---

## 2. 接口定义

### 2.1 图像去噪 (Denoising)

#### 请求

```
POST /api/denoising
Content-Type: multipart/form-data
```

| 参数名  | 类型   | 必填 | 描述             |
| ------- | ------ | ---- | ---------------- |
| `image` | `File` | ✅   | 待去噪的图像文件 |

#### 响应

```typescript
interface DenoisingResponse {
  noisy_img: string; // 添加噪声后的图像 (base64)
  denoised_image: string; // 去噪后的图像 (base64)
}
```

#### 示例

```bash
curl -X POST http://localhost:9000/api/denoising \
  -F "image=@photo.jpg"
```

---

### 2.2 图像分类 (Classification)

#### 请求

```
POST /api/classification
Content-Type: multipart/form-data
```

| 参数名  | 类型   | 必填 | 描述             |
| ------- | ------ | ---- | ---------------- |
| `image` | `File` | ✅   | 待分类的图像文件 |

#### 响应

```typescript
interface ClassificationResponse {
  result: string; // 分类结果标签
}
```

#### 示例

```bash
curl -X POST http://localhost:9000/api/classification \
  -F "image=@photo.jpg"
```

---

### 2.3 相似检索 (Similarity)

#### 请求

```
POST /api/simimages
Content-Type: multipart/form-data
```

| 参数名       | 类型   | 必填 | 默认值 | 描述               |
| ------------ | ------ | ---- | ------ | ------------------ |
| `image`      | `File` | ✅   | -      | 待检索的图像文件   |
| `num_images` | `int`  | ❌   | `10`   | 返回的相似图像数量 |

#### 响应

```typescript
interface SimilarityResponse {
  image_urls: string[]; // 相似图像 URL 列表
}
```

#### 示例

```bash
curl -X POST http://localhost:9000/api/simimages \
  -F "image=@photo.jpg" \
  -F "num_images=10"
```

---

### 2.4 健康检查 (Health)

#### 请求

```
GET /api/health
HEAD /api/health
```

#### 响应

```typescript
interface HealthResponse {
  status: "healthy";
}
```

---

## 3. 错误码规范

### 3.1 状态码定义

| 枚举名             | 状态码 | 含义       | 说明                |
| ------------------ | ------ | ---------- | ------------------- |
| `SUCCESS`          | 200    | 成功       | 请求处理成功        |
| `BAD_REQUEST`      | 400    | 请求错误   | 参数错误、格式错误  |
| `UNAUTHORIZED`     | 401    | 未授权     | 未登录或 token 过期 |
| `FORBIDDEN`        | 403    | 禁止访问   | 无权限访问资源      |
| `NOT_FOUND`        | 404    | 未找到     | 资源不存在          |
| `SERVER_ERROR`     | 500    | 服务器错误 | 内部处理异常        |
| `VALIDATION_ERROR` | 1001   | 校验失败   | 字段校验不通过      |
| `BUSINESS_ERROR`   | 2000   | 业务错误   | 通用业务逻辑错误    |

### 3.2 业务错误扩展

在 `BUSINESS_ERROR (2000)` 的基础上，可以定义具体的业务错误场景（通过 message 区分或扩展 code）：

| 场景         | 描述                    |
| ------------ | ----------------------- |
| 模型未初始化 | 需要先调用 init_model() |
| 图像格式无效 | 仅支持 JPG/PNG/WebP     |
| 图像过大     | 图像尺寸超过限制        |
| 处理失败     | 模型推理过程异常        |

---

## 4. 前端类型定义

### 4.1 共享类型 (shared/types/api.ts)

```typescript
// 基础响应类型
export enum ApiCode {
  SUCCESS = 200,
  BAD_REQUEST = 400,
  UNAUTHORIZED = 401,
  FORBIDDEN = 403,
  NOT_FOUND = 404,
  VALIDATION_ERROR = 1001,
  BUSINESS_ERROR = 2000,
  SERVER_ERROR = 500,
}

export interface Result<T = any> {
  code: ApiCode | number;
  data: T;
  message: string;
}

export interface PageResult<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

// 图像处理相关类型
export interface DenoisingResult {
  noisy_img: string;
  denoised_image: string;
}

export interface ClassificationResult {
  result: string;
}

export interface SimilarityResult {
  image_urls: string[];
}

// 相似图片项
export interface SimilarImage {
  index: number;
  url: string;
  similarity?: number;
}
```

### 4.2 请求封装示例

```typescript
// composables/useApi.ts
export const useApi = () => {
  const baseUrl = "/api";

  const upload = async <T>(
    endpoint: string,
    formData: FormData
  ): Promise<T> => {
    const response = await fetch(`${baseUrl}${endpoint}`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Request failed");
    }

    return response.json();
  };

  return { upload };
};
```

---

## 5. 后端实现规范

### 5.1 Pydantic 模型定义

```python
# backend/common/schemas.py
from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional, Any
from enum import IntEnum

T = TypeVar("T")

class ApiCode(IntEnum):
    SUCCESS = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    VALIDATION_ERROR = 1001
    BUSINESS_ERROR = 2000
    SERVER_ERROR = 500

class Result(BaseModel, Generic[T]):
    """统一响应格式"""
    code: int = Field(default=ApiCode.SUCCESS, description="业务状态码")
    data: Optional[T] = Field(default=None, description="数据")
    message: str = Field(default="Success", description="提示信息")

```

### 5.2 路由定义规范

```python
# 模块路由定义示例
from fastapi import APIRouter, UploadFile, File, HTTPException
from .schemas import DenoisingResponse
from common.schemas import Result, ApiCode

router = APIRouter(
    prefix="/denoising",
    tags=["图像去噪"]
)

@router.post("", response_model=Result[DenoisingResponse])
async def denoise(
    image: UploadFile = File(..., description="待处理的图像")
):
    """图像去噪处理"""
    try:
        # 业务逻辑获取结果
        result_data = ...

        return Result(
            code=ApiCode.SUCCESS,
            data=result_data,
            message="去噪成功"
        )
    except Exception as e:
        # 全局异常处理器通常会捕获这个，这里仅作演示
        return Result(
            code=ApiCode.SERVER_ERROR,
            message=str(e)
        )
```

---

## 6. 命名规范

### 6.1 变量命名

| 语言       | 风格       | 示例                           |
| ---------- | ---------- | ------------------------------ |
| Python     | snake_case | `denoised_image`, `num_images` |
| TypeScript | camelCase  | `denoisedImage`, `numImages`   |
| URL 参数   | snake_case | `num_images`, `image_url`      |

### 6.2 字段映射

前后端字段保持一致性：

| 后端 (Python)    | 前端 (TypeScript) | 说明     |
| ---------------- | ----------------- | -------- |
| `noisy_img`      | `noisy_img`       | 保持一致 |
| `denoised_image` | `denoised_image`  | 保持一致 |
| `image_urls`     | `image_urls`      | 保持一致 |

> **注意**: 由于使用 JSON 传输，前端直接使用后端的 snake_case 命名，避免额外的转换开销。

---

## 7. 版本控制

### 7.1 API 版本

当前版本：`v1`（隐式版本，无前缀）

未来版本升级时使用路径版本：

- `v1`: `/api/denoising`
- `v2`: `/api/v2/denoising`

### 7.2 变更策略

| 变更类型     | 是否破坏兼容 | 处理方式                     |
| ------------ | ------------ | ---------------------------- |
| 新增字段     | ❌           | 直接添加，客户端忽略未知字段 |
| 删除字段     | ✅           | 新版本 + 过渡期              |
| 修改字段类型 | ✅           | 新版本                       |
| 新增端点     | ❌           | 直接添加                     |
| 删除端点     | ✅           | 标记废弃 → 新版本移除        |

---

## 8. 文件结构

```
backend/
├── apps/
│   └── image_processing/
│       ├── denoising/
│       │   ├── __init__.py
│       │   ├── routes.py      # API 路由
│       │   ├── schemas.py     # Pydantic 模型
│       │   ├── service.py     # 业务逻辑
│       │   └── model.py       # 模型定义
│       ├── classification/
│       │   └── ...
│       └── similarity/
│           └── ...
└── common/
    ├── schemas.py             # 通用模型
    └── exceptions.py          # 自定义异常

frontend/
├── composables/
│   └── useImageProcess.ts     # API 调用封装
├── types/
│   └── api.d.ts               # 类型定义
└── utils/
    └── request.ts             # HTTP 请求工具
```

---

## 9. 测试示例

### 9.1 后端测试

```python
# tests/test_denoising.py
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_denoising_success():
    with open("test_image.jpg", "rb") as f:
        response = client.post(
            "/api/denoising",
            files={"image": ("test.jpg", f, "image/jpeg")}
        )
    assert response.status_code == 200
    res = response.json()
    assert res["code"] == 200
    assert "noisy_img" in res["data"]
    assert "denoised_image" in res["data"]
```

### 9.2 前端测试

```typescript
// tests/useImageProcess.test.ts
import { describe, it, expect } from "vitest";
import { useImageProcess } from "~/composables/useImageProcess";

describe("useImageProcess", () => {
  it("should denoise image", async () => {
    const { denoise, denoisedImage } = useImageProcess();
    // Mock and test
  });
});
```
