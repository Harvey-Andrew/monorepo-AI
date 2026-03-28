@echo off
chcp 65001 >nul
echo ========================================
echo    Chat 模块依赖安装脚本
echo    Conda环境: chat_module
echo ========================================
echo.

echo [1/4] 创建 Conda 环境 chat_module (Python 3.12)...
call conda create -n chat_module python=3.12 -y

echo.
echo [2/4] 激活 Conda 环境...
call conda activate chat_module

echo.
echo [3/4] 配置清华镜像源...
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo [4/4] 安装依赖...
pip install -r requirements.txt

echo.
echo ========================================
echo    安装完成！
echo    使用命令激活环境: conda activate chat_module
echo ========================================
pause
