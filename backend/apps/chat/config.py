"""
Chat Module Configuration
"""

import os

# Gemini API Configuration
# 方式1: 直接填写（推荐开发时使用）
_DEFAULT_KEY = "AIzaSyDZaYiYgfyqVGGg7WaoxzWBM5w5_dgqDv8"
# 方式2: 从环境变量读取（生产环境）
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "") or _DEFAULT_KEY
MODEL_NAME = "models/gemini-flash-latest"

# Chat Configuration
MAX_HISTORY_LENGTH = 50  # 最大历史消息数
DEFAULT_SYSTEM_PROMPT = "你是一个有帮助的AI助手，请用中文回答问题。"
