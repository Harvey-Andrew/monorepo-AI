"""
工程化脚本 - 依赖安装

遍历 backend/apps 目录，安装每个模块的 requirements.txt
"""

import os
import subprocess
import sys
from pathlib import Path


def install_deps():
    """安装所有模块依赖"""
    # 获取 backend 目录
    script_dir = Path(__file__).parent
    backend_dir = script_dir.parent / "backend"
    apps_dir = backend_dir / "apps"

    # 安装基础依赖
    base_requirements = backend_dir / "requirements.txt"
    if base_requirements.exists():
        print(f"安装基础依赖: {base_requirements}")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(base_requirements)],
            check=True,
        )

    # 遍历 apps 目录
    if not apps_dir.exists():
        print(f"apps 目录不存在: {apps_dir}")
        return

    for app_dir in apps_dir.iterdir():
        if not app_dir.is_dir():
            continue

        requirements = app_dir / "requirements.txt"
        if requirements.exists():
            # 检查是否有实际依赖（排除注释和空行）
            with open(requirements, "r", encoding="utf-8") as f:
                deps = [
                    line.strip()
                    for line in f
                    if line.strip() and not line.startswith("#")
                ]

            if deps:
                print(f"安装 {app_dir.name} 依赖: {requirements}")
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "-r", str(requirements)],
                    check=True,
                )


if __name__ == "__main__":
    install_deps()
    print("依赖安装完成！")
