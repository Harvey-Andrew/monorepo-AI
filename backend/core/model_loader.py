"""
模型加载器

支持按版本号加载模型，缓存已加载模型
"""

import torch
from pathlib import Path
from typing import Dict, Any, Optional
from functools import lru_cache
from .config import settings


class ModelLoader:
    """模型加载器"""

    def __init__(self):
        self._cache: Dict[str, Any] = {}
        self._device = self._detect_device()

    def _detect_device(self) -> torch.device:
        """检测可用设备"""
        if settings.default_device == "cuda" and torch.cuda.is_available():
            return torch.device("cuda")
        return torch.device("cpu")

    @property
    def device(self) -> torch.device:
        """获取当前设备"""
        return self._device

    def load(
        self,
        app: str,
        model_name: str,
        version: str = "default",
        model_class: Optional[type] = None,
    ) -> Any:
        """
        加载模型

        Args:
            app: 应用名称 (如 'denoising', 'classification')
            model_name: 模型文件名 (如 'model.pt')
            version: 版本号 (如 'v1.0', 'default')
            model_class: 模型类，用于实例化

        Returns:
            加载的模型实例
        """
        cache_key = f"{app}/{version}/{model_name}"

        if cache_key in self._cache:
            return self._cache[cache_key]

        model_path = settings.models_dir / app / version / model_name

        if not model_path.exists():
            raise FileNotFoundError(f"模型文件不存在: {model_path}")

        # 加载权重
        state_dict = torch.load(model_path, map_location=self._device)

        if model_class is not None:
            # 如果提供了模型类，实例化并加载权重
            model = model_class()
            model.load_state_dict(state_dict)
            model.to(self._device)
            model.eval()
        else:
            # 否则直接返回 state_dict
            model = state_dict

        self._cache[cache_key] = model
        return model

    def clear_cache(self, app: Optional[str] = None):
        """清除模型缓存"""
        if app is None:
            self._cache.clear()
        else:
            keys_to_remove = [k for k in self._cache if k.startswith(f"{app}/")]
            for key in keys_to_remove:
                del self._cache[key]


# 全局模型加载器实例
model_loader = ModelLoader()
