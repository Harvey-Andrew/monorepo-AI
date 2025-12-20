# 智图寻宝 Monorepo - 问题排查与修复记录

## 问题 1：Vue 模板解析错误

### 错误信息

```
Attribute name cannot contain U+0022 ("), U+0027 ('), and U+003C (<).
```

### 原因

`index.vue` 中的 `placeholder` 属性包含中文双引号 `"..."`，Vue 模板解析器无法正确处理。

### 修复方案

将中文双引号 `"..."` 改为中文书名号 `「...」`：

```vue
<!-- 错误 -->
placeholder="点击"商品分类"按钮获取结果..."

<!-- 正确 -->
placeholder='点击「商品分类」按钮获取结果...'
```

---

## 问题 2：图像去噪 API 返回 undefined

### 错误信息

```
GET data:image/png;base64,undefined net::ERR_INVALID_URL
```

### 原因

Flask 后端使用 `json.dumps()` 返回 JSON，且 `Content-Type` header 写错为 `ContentType`，导致前端无法正确解析响应。

### 修复方案

使用 Flask 的 `jsonify()` 替代 `json.dumps()`：

```python
# 错误
return (
    json.dumps({"noisy_img": ..., "denoised_image": ...}),
    200,
    {"ContentType": "application/json"},
)

# 正确
return jsonify({
    "noisy_img": encode_image(noisy_img),
    "denoised_image": encode_image(denoised_image)
})
```

---

## 问题 3：Python 启动脚本在 Windows 上失败

### 错误信息

```
Python 进程退出，代码: null
```

### 原因

`conda run -n env python script.py` 命令在 Windows 上通过 Node.js 子进程调用时兼容性差。

### 修复方案

改用 `cmd /c conda activate env && python script.py`：

```javascript
// 错误
spawn('conda', ['run', '-n', condaEnv, 'python', scriptPath], {...});

// 正确 (Windows)
const cmd = `conda activate ${condaEnv} && python ${scriptPath}`;
spawn('cmd', ['/c', cmd], { cwd: pythonDir, stdio: 'inherit' });
```

---

## 问题 4：Python 路径引号错误

### 错误信息

```
python: can't open file '...python\\"D:\\...\\web_app.py"': [Errno 22] Invalid argument
```

### 原因

使用绝对路径时，路径被双重引用。

### 修复方案

改用相对路径，因为 `cwd` 已经设置为 python 目录：

```javascript
// 错误
const scriptPath = join(pythonDir, "web_app.py");
const cmd = `conda activate ${condaEnv} && python "${scriptPath}"`;

// 正确
const scriptPath = "web_app.py"; // 相对路径
const cmd = `conda activate ${condaEnv} && python ${scriptPath}`;
```

---

## 问题 5：flask-cors 未安装

### 错误信息

```
警告: flask-cors 未安装，跨域请求可能被阻止
```

### 修复方案

安装 flask-cors：

```bash
conda activate deeplearning
pip install flask-cors
```

---

## 问题 6：端口被占用

### 错误信息

```
WebSocket server error: Port 24678 is already in use
[get-port] Unable to find an available port (tried 3000 on host "localhost")
```

### 原因

之前的 Nuxt 进程未正确关闭。

### 修复方案

1. 使用 Ctrl+C 停止所有运行中的终端进程
2. 或手动结束占用端口的进程：

```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

---

## 问题 7：相似商品图片 404

### 错误信息

```
GET http://localhost:3001/dataset/3813.jpg 404 (Page not found)
```

### 原因

`packages/client/public/` 目录中没有 `dataset` 文件夹，图片数据集位于项目根目录。

### 修复方案

在 `nuxt.config.ts` 中配置 devProxy 将 `/dataset` 请求转发到 Python 后端：

```typescript
nitro: {
    devProxy: {
        '/dataset': {
            target: 'http://localhost:9000/dataset',
            changeOrigin: true
        }
    }
}
```

---

## 问题 8：相似推荐数量参数不生效

### 错误信息

前端修改推荐数量后，后端仍返回默认 10 条数据。

### 原因

Nuxt API 代理层 (`simimages.post.ts`) 只转发了 `image` 字段，忽略了 `num_images` 参数。

### 修复方案

修改 `server/api/simimages.post.ts`，添加 `num_images` 字段的转发：

```typescript
for (const field of formData) {
  if (field.name === "image" && field.data) {
    body.append("image", new Blob([field.data]), field.filename || "image.png");
  } else if (field.name === "num_images" && field.data) {
    // 转发推荐数量参数
    body.append("num_images", field.data.toString());
  }
}
```

---

## 问题 9：页面文本选择光标问题

### 错误信息

点击页面任何位置出现文本选择光标（I-beam cursor）。

### 原因

页面元素默认允许文本选择。

### 修复方案

在页面容器样式中禁用文本选择：

```css
.page-container {
  user-select: none;
}
```

---

## 问题 10：图片预览按钮被遮挡

### 错误信息

点击图片上的操作按钮（重新选择、删除）时，触发了图片全屏预览。

### 原因

悬浮操作容器 `.hover-actions` 设置了 `pointer-events: auto`，挡住了图片点击。

### 修复方案

让容器始终 `pointer-events: none`，只有按钮本身可点击：

```css
.hover-actions {
  pointer-events: none;
}

.hover-actions .reselect-btn,
.hover-actions .delete-btn {
  pointer-events: auto;
}
```

---

## 问题 11：oxc-parser Native Binding 安装失败

### 错误信息

```
ERROR  Cannot find native binding. npm has a bug related to optional dependencies
Cannot find module '@oxc-parser/binding-win32-x64-msvc'
```

### 原因

`oxc-parser` 包依赖平台特定的 native binding（如 `@oxc-parser/binding-win32-x64-msvc`），但 npm/pnpm 处理可选依赖时存在已知 bug，导致 native binding 未正确安装。

参考：https://github.com/npm/cli/issues/4828

### 修复方案

1. 手动安装缺失的 native binding（使用 `--ignore-scripts` 避免触发 postinstall）：

```bash
pnpm add @oxc-parser/binding-win32-x64-msvc -D -w --ignore-scripts
```

2. 强制重新安装所有依赖：

```bash
pnpm install --force
```

---

## 问题 12：Node.js 连接 localhost 时 IPv6 连接被拒绝

### 错误信息

```
connect ECONNREFUSED ::1:9000
[POST] "http://localhost:9000/denoising": <no response> fetch failed
```

### 原因

Node.js 在解析 `localhost` 时优先使用 IPv6 地址 (`::1`)，但 Python Flask 默认只在 IPv4 地址 (`127.0.0.1`) 上监听，导致连接被拒绝。

### 修复方案

在 `nuxt.config.ts` 中将 `localhost` 改为明确的 IPv4 地址 `127.0.0.1`：

```typescript
// 错误
pythonApiBase: "http://localhost:9000";

// 正确
pythonApiBase: "http://127.0.0.1:9000";
```

同样修改 `devProxy` 配置：

```typescript
devProxy: {
    '/dataset': {
        target: 'http://127.0.0.1:9000/dataset',  // 使用 127.0.0.1 而非 localhost
        changeOrigin: true
    }
}
```

---

## 总结检查清单

| 检查项                      | 状态   |
| --------------------------- | ------ |
| Vue 模板无非法引号字符      | ✅     |
| Flask API 使用 jsonify()    | ✅     |
| Python 启动脚本适配 Windows | ✅     |
| flask-cors 已安装           | ✅     |
| dataset 代理已配置          | ✅     |
| API 代理正确转发所有参数    | ✅     |
| 页面交互正常（无干扰光标）  | ✅     |
| 图片操作按钮可正常点击      | ✅     |
| native binding 已正确安装   | ✅     |
| API 地址使用 127.0.0.1      | ✅     |
| 端口未被占用                | 需确认 |

---

## 开发建议

1. **清理冗余代码** - 定期检查未使用的组件和导入，保持代码整洁
2. **API 代理层** - 添加新参数时，记得在 Nuxt API 代理层同步转发
3. **跨域问题** - 使用 Nitro devProxy 或确保 flask-cors 已安装
4. **Windows 兼容** - 注意路径分隔符和命令行差异
