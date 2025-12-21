"""
配置管理模块

从环境变量和配置文件加载应用配置
"""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置"""

    # 应用基本配置
    app_name: str = "My Local AI Hub"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 9000

    # 路径配置
    base_dir: Path = Path(__file__).parent.parent
    storage_dir: Path = base_dir / "storage"
    models_dir: Path = storage_dir / "models"
    datasets_dir: Path = storage_dir / "datasets"

    # 模型配置
    default_device: str = "cuda"  # cuda 或 cpu，自动检测

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()


# 导出配置实例
settings = get_settings()
