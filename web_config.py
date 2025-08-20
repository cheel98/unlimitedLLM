#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web应用配置模块
作者: Unlimited AI Team
版本: 1.0.0
"""

import os
from pathlib import Path
from typing import Dict, Any

try:
    from dotenv import load_dotenv
except ImportError:
    print("警告: python-dotenv未安装，将使用系统环境变量")
    load_dotenv = None

class WebConfig:
    """Web应用配置类"""
    
    def __init__(self, env_file: str = ".env"):
        """初始化配置"""
        self.env_file = env_file
        self._load_env()
        self._setup_config()
    
    def _load_env(self):
        """加载环境变量"""
        env_path = Path(self.env_file)
        if env_path.exists() and load_dotenv:
            load_dotenv(env_path)
            print(f"✅ 已加载环境配置: {env_path}")
        elif env_path.exists():
            print(f"⚠️ 找到配置文件但无法加载: {env_path}")
        else:
            print(f"⚠️ 配置文件不存在: {env_path}，使用默认配置")
    
    def _setup_config(self):
        """设置配置参数"""
        # Web服务器配置
        self.WEB_HOST = os.getenv('WEB_HOST', '127.0.0.1')
        self.WEB_PORT = int(os.getenv('WEB_PORT', '5000'))
        self.WEB_DEBUG = os.getenv('WEB_DEBUG', 'false').lower() == 'true'
        self.SECRET_KEY = os.getenv('SECRET_KEY', 'unlimited-agent-secret-key')
        
        # 模型配置
        self.DEFAULT_MODEL_REPO = os.getenv('DEFAULT_MODEL_REPO', 
            'DavidAU/OpenAi-GPT-oss-20b-abliterated-uncensored-NEO-Imatrix-gguf')
        self.DEFAULT_MODEL_FILENAME = os.getenv('DEFAULT_MODEL_FILENAME', 
            'OpenAI-20B-NEO-CODE-DI-Uncensored-Q5_1.gguf')
        self.DEFAULT_MODEL_NAME = os.getenv('DEFAULT_MODEL_NAME', 'OpenAI GPT 20B')
        self.USE_PRETRAINED = os.getenv('USE_PRETRAINED', 'true').lower() == 'true'
        
        # 模型参数
        self.MODEL_CONFIG = {
            'n_ctx': int(os.getenv('MODEL_N_CTX', '4096')),
            'n_threads': int(os.getenv('MODEL_N_THREADS', '8')),
            'n_gpu_layers': int(os.getenv('MODEL_N_GPU_LAYERS', '0')),
            'temperature': float(os.getenv('MODEL_TEMPERATURE', '0.7')),
            'top_p': float(os.getenv('MODEL_TOP_P', '0.9')),
            'top_k': int(os.getenv('MODEL_TOP_K', '40')),
            'repeat_penalty': float(os.getenv('MODEL_REPEAT_PENALTY', '1.1')),
            'max_tokens': int(os.getenv('MODEL_MAX_TOKENS', '2048')),
        }
        
        # 其他配置
        self.MAX_HISTORY_LENGTH = int(os.getenv('MAX_HISTORY_LENGTH', '50'))
        self.THEME = os.getenv('THEME', 'dark')
        self.DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
        self.MODELS_DIR = os.getenv('MODELS_DIR', './models')
        self.HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_TOKEN', '')
    
    def get_model_config(self) -> Dict[str, Any]:
        """获取模型配置"""
        return {
            'model_repo': self.DEFAULT_MODEL_REPO,
            'model_filename': self.DEFAULT_MODEL_FILENAME,
            'model_name': self.DEFAULT_MODEL_NAME,
            'use_pretrained': self.USE_PRETRAINED,
            'model_config': self.MODEL_CONFIG
        }
    
    def get_web_config(self) -> Dict[str, Any]:
        """获取Web配置"""
        return {
            'host': self.WEB_HOST,
            'port': self.WEB_PORT,
            'debug': self.WEB_DEBUG,
            'secret_key': self.SECRET_KEY
        }
    
    def __str__(self) -> str:
        """配置信息字符串表示"""
        return f"""Web配置:
  - 主机: {self.WEB_HOST}:{self.WEB_PORT}
  - 调试: {self.WEB_DEBUG}
  - 主题: {self.THEME}
  
模型配置:
  - 仓库: {self.DEFAULT_MODEL_REPO}
  - 文件: {self.DEFAULT_MODEL_FILENAME}
  - 名称: {self.DEFAULT_MODEL_NAME}
  - 预训练: {self.USE_PRETRAINED}
  
模型参数:
  - 上下文长度: {self.MODEL_CONFIG['n_ctx']}
  - 温度: {self.MODEL_CONFIG['temperature']}
  - 最大令牌: {self.MODEL_CONFIG['max_tokens']}"""

# 全局配置实例
config = WebConfig()

if __name__ == "__main__":
    print("🔧 Web配置信息:")
    print(config)