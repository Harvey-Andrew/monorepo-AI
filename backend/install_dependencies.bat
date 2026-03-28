@echo off
chcp 65001 >nul
echo ========================================
echo    Backend 服务依赖安装脚本
echo    Conda环境: monorepo_backend
echo ========================================
echo.

echo 请选择 PyTorch 版本:
echo [1] GPU 版本 (CUDA 12.1) - 默认
echo [2] GPU 版本 (CUDA 12.4)
echo [3] GPU 版本 (CUDA 11.8)
echo [4] CPU 版本
echo [5] 自定义 CUDA 版本
echo.
set /p choice="请输入选择 (直接回车选择1): "

if "%choice%"=="" set choice=1

if "%choice%"=="1" (
    set PYTORCH_CMD=pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
    set VERSION_DESC=GPU (CUDA 12.1^)
) else if "%choice%"=="2" (
    set PYTORCH_CMD=pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
    set VERSION_DESC=GPU (CUDA 12.4^)
) else if "%choice%"=="3" (
    set PYTORCH_CMD=pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    set VERSION_DESC=GPU (CUDA 11.8^)
) else if "%choice%"=="4" (
    set PYTORCH_CMD=pip3 install torch torchvision torchaudio
    set VERSION_DESC=CPU
) else if "%choice%"=="5" (
    echo.
    echo 常见 CUDA 版本: cu118, cu121, cu124
    set /p cuda_ver="请输入 CUDA 版本号 (例如 cu121): "
    set PYTORCH_CMD=pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/!cuda_ver!
    set VERSION_DESC=GPU (自定义: !cuda_ver!^)
) else (
    echo 无效选择，使用默认 GPU (CUDA 12.1)
    set PYTORCH_CMD=pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
    set VERSION_DESC=GPU (CUDA 12.1^)
)

setlocal enabledelayedexpansion
echo.
echo 已选择: !VERSION_DESC!
echo.

echo [1/5] 创建 Conda 环境 monorepo_backend (Python 3.12)...
call conda create -n monorepo_backend python=3.12 -y

echo.
echo [2/5] 激活 Conda 环境...
call conda activate monorepo_backend

echo.
echo [3/5] 配置清华镜像源...
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo [4/5] 安装 PyTorch (!VERSION_DESC!)...
!PYTORCH_CMD!

echo.
echo [5/5] 安装服务依赖...
pip install -r requirements.txt

echo.
echo ========================================
echo    安装完成！
echo    PyTorch 版本: !VERSION_DESC!
echo    使用命令激活环境: conda activate monorepo_backend
echo    启动服务: python app.py
echo ========================================
endlocal
pause
