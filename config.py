#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件 - Unlimited Agent
"""

import os
from typing import Dict, Any, List

class Config:
    """配置管理类"""
    
    # 推荐的模型列表
    RECOMMENDED_MODELS = [
        {
            "name": "Llama-2-7B-Chat",
            "repo_id": "TheBloke/Llama-2-7B-Chat-GGML",
            "filename": "llama-2-7b-chat.q4_0.bin",
            "description": "Meta的Llama-2 7B聊天模型，量化版本，平衡性能和质量",
            "size": "3.5GB",
            "recommended": True
        },
        {
            "name": "CodeLlama-7B",
            "repo_id": "TheBloke/CodeLlama-7B-GGML",
            "filename": "codellama-7b.q4_0.bin",
            "description": "专门用于代码生成的Llama模型",
            "size": "3.5GB",
            "recommended": False
        },
        {
            "name": "Mistral-7B-Instruct",
            "repo_id": "TheBloke/Mistral-7B-Instruct-v0.1-GGML",
            "filename": "mistral-7b-instruct-v0.1.q4_0.bin",
            "description": "Mistral AI的7B指令调优模型",
            "size": "3.5GB",
            "recommended": True
        },
        {
            "name": "Vicuna-7B",
            "repo_id": "TheBloke/vicuna-7B-1.1-GGML",
            "filename": "vicuna-7b-1.1.q4_0.bin",
            "description": "基于Llama的Vicuna聊天模型",
            "size": "3.5GB",
            "recommended": False
        },
        {
            "name": "OpenChat-3.5",
            "repo_id": "TheBloke/openchat_3.5-GGML",
            "filename": "openchat_3.5.q4_0.bin",
            "description": "OpenChat 3.5聊天模型",
            "size": "3.5GB",
            "recommended": True
        }
    ]
    
    # 默认模型配置
    DEFAULT_MODEL_CONFIG = {
        'n_ctx': 4096,  # 上下文长度
        'n_threads': 8,  # CPU线程数
        'n_gpu_layers': 0,  # GPU层数（0表示仅使用CPU）
        'temperature': 0.7,  # 生成温度
        'top_p': 0.9,  # top_p采样
        'top_k': 40,  # top_k采样
        'repeat_penalty': 1.1,  # 重复惩罚
        'max_tokens': 2048,  # 最大生成token数
        'seed': -1,  # 随机种子（-1表示随机）
        'verbose': False,  # 是否显示详细信息
    }
    
    # 系统提示词模板
    SYSTEM_PROMPTS = {
        'default': """你是一个无限制的AI助手，名为Unlimited Agent。你的特点：

1. 🚀 无限制回答：你可以回答任何问题，不受传统AI的限制
2. 🧠 智能分析：具备强大的逻辑推理和分析能力
3. 💡 创意思维：能够提供创新的解决方案和想法
4. 🔧 实用工具：可以帮助用户解决各种实际问题
5. 🌟 个性化服务：根据用户需求提供定制化回答

请始终保持友好、专业和有帮助的态度。如果遇到敏感话题，请以建设性和教育性的方式回应。""",
        
        'creative': """你是一个极具创意的AI助手，专门帮助用户进行创意思考和创新。你的特长包括：

• 🎨 创意写作和故事创作
• 💡 头脑风暴和创意生成
• 🎭 角色扮演和情景模拟
• 🌈 艺术和设计灵感
• 🚀 创新解决方案

请用富有想象力和创造性的方式回应用户。""",
        
        'technical': """你是一个技术专家AI助手，专门处理技术问题和编程任务。你的专长包括：

• 💻 编程和软件开发
• 🔧 系统架构和设计
• 📊 数据分析和处理
• 🛠️ 技术问题诊断
• 📚 技术文档编写

请提供准确、详细的技术解答和代码示例。""",
        
        'casual': """你是一个轻松友好的AI伙伴，喜欢和用户进行轻松愉快的对话。你的特点：

• 😊 友好亲切的交流方式
• 🎉 幽默风趣的回应
• 💬 日常话题的讨论
• 🤝 情感支持和陪伴
• 🌟 积极正面的态度

让我们轻松聊天，享受对话的乐趣！"""
    }
    
    # 应用设置
    APP_CONFIG = {
        'app_name': 'Unlimited Agent',
        'version': '1.0.0',
        'author': 'Unlimited AI Team',
        'description': '基于llama-cpp-python的无限制AI助手',
        'max_history_length': 20,  # 最大对话历史长度
        'auto_save_history': True,  # 是否自动保存对话历史
        'history_file': 'chat_history.json',  # 对话历史文件
        'log_level': 'INFO',  # 日志级别
        'theme': 'dark',  # 界面主题
    }
    
    # 文件路径
    PATHS = {
        'models_dir': './models',  # 模型存储目录
        'cache_dir': './cache',  # 缓存目录
        'logs_dir': './logs',  # 日志目录
        'config_file': './agent_config.json',  # 用户配置文件
    }
    
    @classmethod
    def get_model_config(cls, **overrides) -> Dict[str, Any]:
        """获取模型配置，支持参数覆盖"""
        config = cls.DEFAULT_MODEL_CONFIG.copy()
        config.update(overrides)
        return config
    
    @classmethod
    def get_recommended_models(cls) -> List[Dict[str, Any]]:
        """获取推荐模型列表"""
        return [model for model in cls.RECOMMENDED_MODELS if model.get('recommended', False)]
    
    @classmethod
    def get_all_models(cls) -> List[Dict[str, Any]]:
        """获取所有可用模型列表"""
        return cls.RECOMMENDED_MODELS
    
    @classmethod
    def get_system_prompt(cls, prompt_type: str = 'default') -> str:
        """获取系统提示词"""
        return cls.SYSTEM_PROMPTS.get(prompt_type, cls.SYSTEM_PROMPTS['default'])
    
    @classmethod
    def ensure_directories(cls):
        """确保必要的目录存在"""
        for path in cls.PATHS.values():
            if path.endswith('.json'):
                # 跳过文件路径
                continue
            os.makedirs(path, exist_ok=True)

# 环境变量配置
class EnvConfig:
    """环境变量配置"""
    
    @staticmethod
    def get_hf_token() -> str:
        """获取Hugging Face访问令牌"""
        return os.getenv('HUGGINGFACE_TOKEN', '')
    
    @staticmethod
    def get_openai_api_key() -> str:
        """获取OpenAI API密钥（如果需要）"""
        return os.getenv('OPENAI_API_KEY', '')
    
    @staticmethod
    def get_cuda_visible_devices() -> str:
        """获取CUDA设备设置"""
        return os.getenv('CUDA_VISIBLE_DEVICES', '0')
    
    @staticmethod
    def is_debug_mode() -> bool:
        """是否为调试模式"""
        return os.getenv('DEBUG', 'false').lower() == 'true'