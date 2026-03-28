@echo off
chcp 65001 >nul
echo ========================================
echo    Monorepo 全栈项目依赖安装脚本
echo    包含前端 (Node.js) 和后端 (Python)
echo    默认: 一键安装全部 + GPU (CUDA 12.1)
echo ========================================
echo.

echo 请选择安装模式:
echo [直接回车] 一键安装全部 (前端 + 后端, CUDA 12.1) - 推荐
echo [2] 仅安装前端 (Node.js)
echo [3] 仅安装后端 (Python, 可选 CUDA 版本)
echo.
set /p install_choice="请输入选择: "

:: 默认一键安装
if "%install_choice%"=="" (
    set install_choice=1
    set PYTORCH_CMD=pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
    set VERSION_DESC=GPU (CUDA 12.1^)
    goto auto_install
)

if "%install_choice%"=="2" goto install_frontend_only
if "%install_choice%"=="3" goto install_backend_custom

:: 选项 1 也是一键安装
set PYTORCH_CMD=pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
set VERSION_DESC=GPU (CUDA 12.1^)
goto auto_install

:: ========================================
:: 一键自动安装 (前端 + 后端)
:: ========================================
:auto_install
setlocal enabledelayedexpansion
echo.
echo [模式] 一键安装: 前端 + 后端 (PyTorch !VERSION_DESC!)
echo.

:: 安装前端
echo ========================================
echo    安装前端依赖
echo ========================================
echo.

where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Node.js，请先安装 Node.js 18+
    echo 下载地址: https://nodejs.org/
    goto install_backend_auto
)

where pnpm >nul 2>nul
if %errorlevel% neq 0 (
    echo [提示] 未检测到 pnpm，正在安装...
    npm install -g pnpm
)

echo [前端] 安装依赖...
call pnpm install
echo [前端] 完成！

:install_backend_auto
echo.
echo ========================================
echo    安装后端依赖
echo ========================================
echo.

echo [后端] 创建 Conda 环境 monorepo_backend (Python 3.12)...
call conda create -n monorepo_backend python=3.12 -y

echo.
echo [后端] 激活 Conda 环境...
call conda activate monorepo_backend

echo.
echo [后端] 配置清华镜像源...
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo [后端] 安装 PyTorch (!VERSION_DESC!)...
!PYTORCH_CMD!

echo.
echo [后端] 安装服务依赖...
pip install -r backend/requirements.txt

echo [后端] 完成！
goto finish

:: ========================================
:: 仅安装前端
:: ========================================
:install_frontend_only
echo.
echo ========================================
echo    仅安装前端依赖
echo ========================================
echo.

where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Node.js，请先安装 Node.js 18+
    goto finish
)

where pnpm >nul 2>nul
if %errorlevel% neq 0 (
    echo [提示] 未检测到 pnpm，正在安装...
    npm install -g pnpm
)

echo [前端] 安装依赖...
call pnpm install
echo [前端] 完成！
goto finish

:: ========================================
:: 仅安装后端 (可选 CUDA 版本)
:: ========================================
:install_backend_custom
echo.
echo ========================================
echo    仅安装后端依赖
echo ========================================
echo.
echo 请选择 PyTorch 版本:
echo [1] GPU 版本 (CUDA 12.1) - 默认
echo [2] GPU 版本 (CUDA 12.4)
echo [3] GPU 版本 (CUDA 11.8)
echo [4] CPU 版本
echo [5] 自定义 CUDA 版本
echo.
set /p pytorch_choice="请输入选择 (直接回车选择1): "

if "%pytorch_choice%"=="" set pytorch_choice=1

if "%pytorch_choice%"=="1" (
    set PYTORCH_CMD=pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
    set VERSION_DESC=GPU (CUDA 12.1^)
) else if "%pytorch_choice%"=="2" (
    set PYTORCH_CMD=pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
    set VERSION_DESC=GPU (CUDA 12.4^)
) else if "%pytorch_choice%"=="3" (
    set PYTORCH_CMD=pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    set VERSION_DESC=GPU (CUDA 11.8^)
) else if "%pytorch_choice%"=="4" (
    set PYTORCH_CMD=pip3 install torch torchvision torchaudio
    set VERSION_DESC=CPU
) else if "%pytorch_choice%"=="5" (
    echo.
    echo 常见 CUDA 版本: cu118, cu121, cu124
    set /p cuda_ver="请输入 CUDA 版本号 (例如 cu121): "
    set PYTORCH_CMD=pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/!cuda_ver!
    set VERSION_DESC=GPU (自定义: !cuda_ver!^)
) else (
    set PYTORCH_CMD=pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
    set VERSION_DESC=GPU (CUDA 12.1^)
)

setlocal enabledelayedexpansion

echo.
echo [后端] 创建 Conda 环境 monorepo_backend (Python 3.12)...
call conda create -n monorepo_backend python=3.12 -y

echo.
echo [后端] 激活 Conda 环境...
call conda activate monorepo_backend

echo.
echo [后端] 配置清华镜像源...
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo [后端] 安装 PyTorch (!VERSION_DESC!)...
!PYTORCH_CMD!

echo.
echo [后端] 安装服务依赖...
pip install -r backend/requirements.txt

echo [后端] 完成！

:finish
echo.
echo ========================================
echo    安装完成！
echo ========================================
echo.
echo 启动命令:
echo   前端: pnpm dev:client
echo   后端: conda activate monorepo_backend ^&^& pnpm dev:server
echo   全栈: conda activate monorepo_backend ^&^& pnpm dev
echo.
echo ========================================
endlocal
pause
