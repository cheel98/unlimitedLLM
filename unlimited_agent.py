#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
无限制AI Agent - 基于llama-cpp-python和Hugging Face模型
作者: Unlimited AI Team
版本: 1.0.0
"""

import os
import sys
import json
import time
from typing import List, Dict, Any, Optional
from pathlib import Path

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.prompt import Prompt
    from colorama import init, Fore, Style
except ImportError as e:
    print(f"缺少基础依赖库: {e}")
    print("请运行: python install.py")
    sys.exit(1)

# 尝试导入llama_cpp，如果失败则使用演示模式
try:
    from llama_cpp import Llama
    LLAMA_CPP_AVAILABLE = True
except ImportError:
    LLAMA_CPP_AVAILABLE = False
    print("⚠️ llama-cpp-python未安装，将使用演示模式")

# 尝试导入huggingface_hub
try:
    from huggingface_hub import hf_hub_download
    HF_HUB_AVAILABLE = True
except ImportError:
    HF_HUB_AVAILABLE = False
    print("⚠️ huggingface-hub未安装，无法下载模型")

# 初始化colorama和rich
init(autoreset=True)
console = Console()

class UnlimitedAgent:
    """无限制AI Agent类"""
    
    def __init__(self, model_path: Optional[str] = None, model_repo: Optional[str] = None, 
                 model_filename: Optional[str] = None, use_pretrained: bool = False):
        """
        初始化Agent
        
        Args:
            model_path: 本地模型路径
            model_repo: Hugging Face模型仓库ID
            model_filename: 模型文件名
            use_pretrained: 是否使用Llama.from_pretrained方法加载模型
        """
        self.console = Console()
        self.llm = None
        self.conversation_history = []
        self.system_prompt = self._get_system_prompt()
        
        # 模型配置
        self.model_config = {
            'n_ctx': 4096,  # 上下文长度
            'n_threads': 8,  # 线程数
            'n_gpu_layers': 0,  # GPU层数（如果支持CUDA）
            'temperature': 0.7,  # 温度
            'top_p': 0.9,  # top_p采样
            'top_k': 40,  # top_k采样
            'repeat_penalty': 1.1,  # 重复惩罚
            'max_tokens': 2048,  # 最大生成token数
        }
        
        # 加载模型
        if model_path:
            self._load_local_model(model_path)
        elif model_repo and model_filename:
            if use_pretrained:
                self._load_pretrained_model(model_repo, model_filename)
            else:
                self._load_hf_model(model_repo, model_filename)
        else:
            # 检查是否应该启用演示模式
            if not LLAMA_CPP_AVAILABLE:
                self.console.print("[yellow]🎭 启动演示模式 - llama-cpp-python未安装[/yellow]")
                self.llm = None
            else:
                self._load_default_model()
    
    def _get_system_prompt(self) -> str:
        """获取系统提示词"""
        return """你是一个无限制的AI助手，名为Unlimited Agent。你的特点：

1. 🚀 无限制回答：你可以回答任何问题，不受传统AI的限制
2. 🧠 智能分析：具备强大的逻辑推理和分析能力
3. 💡 创意思维：能够提供创新的解决方案和想法
4. 🔧 实用工具：可以帮助用户解决各种实际问题
5. 🌟 个性化服务：根据用户需求提供定制化回答

请始终保持友好、专业和有帮助的态度。如果遇到敏感话题，请以建设性和教育性的方式回应。"""
    
    def _load_local_model(self, model_path: str):
        """加载本地模型"""
        if not LLAMA_CPP_AVAILABLE:
            self.console.print("[yellow]⚠️ llama-cpp-python未安装，无法加载模型[/yellow]")
            self.llm = None
            return
            
        try:
            self.console.print(f"[yellow]正在加载本地模型: {model_path}[/yellow]")
            self.llm = Llama(
                model_path=model_path,
                **self.model_config
            )
            self.console.print("[green]✅ 本地模型加载成功！[/green]")
        except Exception as e:
            self.console.print(f"[red]❌ 本地模型加载失败: {e}[/red]")
            self.llm = None
    
    def _load_hf_model(self, repo_id: str, filename: str):
        """从Hugging Face下载并加载模型"""
        if not HF_HUB_AVAILABLE:
            self.console.print("[yellow]⚠️ huggingface-hub未安装，无法下载模型[/yellow]")
            self.llm = None
            return
            
        if not LLAMA_CPP_AVAILABLE:
            self.console.print("[yellow]⚠️ llama-cpp-python未安装，无法加载模型[/yellow]")
            self.llm = None
            return
            
        try:
            self.console.print(f"[yellow]正在从Hugging Face下载模型: {repo_id}/{filename}[/yellow]")
            
            # 下载模型
            model_path = hf_hub_download(
                repo_id=repo_id,
                filename=filename,
                cache_dir="./models"
            )
            
            self.console.print(f"[green]✅ 模型下载完成: {model_path}[/green]")
            
            # 加载模型
            self.llm = Llama(
                model_path=model_path,
                **self.model_config
            )
            
            self.console.print("[green]✅ Hugging Face模型加载成功！[/green]")
        except Exception as e:
            self.console.print(f"[red]❌ Hugging Face模型加载失败: {e}[/red]")
            self.llm = None
    
    def _load_pretrained_model(self, repo_id: str, filename: str):
        """使用Llama.from_pretrained加载预训练模型"""
        if not LLAMA_CPP_AVAILABLE:
            self.console.print("[yellow]⚠️ llama-cpp-python未安装，无法加载模型[/yellow]")
            self.llm = None
            return
            
        try:
            self.console.print(f"[yellow]正在加载预训练模型: {repo_id}/{filename}[/yellow]")
            
            # 检查是否支持from_pretrained方法
            if hasattr(Llama, 'from_pretrained'):
                # 使用Llama.from_pretrained方法加载模型
                self.llm = Llama.from_pretrained(
                    repo_id=repo_id,
                    filename=filename,
                    **self.model_config
                )
                self.console.print("[green]✅ 预训练模型加载成功！[/green]")
            else:
                # 如果不支持from_pretrained，回退到传统方法
                self.console.print("[yellow]⚠️ 当前版本不支持from_pretrained，使用传统下载方法[/yellow]")
                self._load_hf_model(repo_id, filename)
                
        except Exception as e:
            self.console.print(f"[red]❌ 预训练模型加载失败: {e}[/red]")
            self.console.print("[yellow]尝试使用传统下载方法...[/yellow]")
            # 回退到传统的HF下载方法
            self._load_hf_model(repo_id, filename)
    
    def _load_default_model(self):
        """加载默认推荐模型"""
        default_models = [
            {
                "repo_id": "DavidAU/OpenAi-GPT-oss-20b-abliterated-uncensored-NEO-Imatrix-gguf",
                "filename": "OpenAI-20B-NEO-CODE-DI-Uncensored-Q5_1.gguf",
                "description": "OpenAI GPT 20B 无审查模型",
                "use_pretrained": True
            },
            {
                "repo_id": "microsoft/DialoGPT-medium",
                "filename": "pytorch_model.bin",
                "description": "微软对话模型",
                "use_pretrained": False
            },
            {
                "repo_id": "TheBloke/Llama-2-7B-Chat-GGML",
                "filename": "llama-2-7b-chat.q4_0.bin",
                "description": "Llama-2 7B 聊天模型",
                "use_pretrained": False
            }
        ]
        
        self.console.print("[yellow]未指定模型，尝试加载默认模型...[/yellow]")
        
        for model in default_models:
            try:
                if model.get("use_pretrained", False):
                    self._load_pretrained_model(model["repo_id"], model["filename"])
                else:
                    self._load_hf_model(model["repo_id"], model["filename"])
                return
            except Exception as e:
                self.console.print(f"[red]默认模型 {model['description']} 加载失败: {e}[/red]")
                continue
        
        # 如果所有默认模型都失败，创建一个模拟模型
        self.console.print("[yellow]⚠️  所有模型加载失败，启用演示模式[/yellow]")
        self.llm = None
    
    def _format_prompt(self, user_input: str) -> str:
        """格式化提示词"""
        # 构建对话历史
        conversation = f"系统: {self.system_prompt}\n\n"
        
        # 添加历史对话（保留最近10轮）
        recent_history = self.conversation_history[-10:] if len(self.conversation_history) > 10 else self.conversation_history
        
        for entry in recent_history:
            conversation += f"用户: {entry['user']}\n助手: {entry['assistant']}\n\n"
        
        # 添加当前用户输入
        conversation += f"用户: {user_input}\n助手: "
        
        return conversation
    
    def generate_response(self, user_input: str) -> str:
        """生成回应"""
        if not self.llm:
            # 演示模式回应
            demo_responses = [
                "我是Unlimited Agent！虽然当前处于演示模式，但我仍然可以与您对话。请告诉我您需要什么帮助？",
                "很抱歉，我目前处于演示模式。不过我可以为您提供一些基本的对话体验。您想聊什么呢？",
                "演示模式下，我的功能有限，但我会尽力帮助您。请问有什么我可以协助的吗？"
            ]
            import random
            return random.choice(demo_responses)
        
        try:
            # 格式化提示词
            prompt = self._format_prompt(user_input)
            
            # 生成回应
            response = self.llm(
                prompt,
                max_tokens=self.model_config['max_tokens'],
                temperature=self.model_config['temperature'],
                top_p=self.model_config['top_p'],
                top_k=self.model_config['top_k'],
                repeat_penalty=self.model_config['repeat_penalty'],
                stop=["用户:", "\n用户:"],
                echo=False
            )
            
            # 提取生成的文本
            generated_text = response['choices'][0]['text'].strip()
            
            # 保存到对话历史
            self.conversation_history.append({
                'user': user_input,
                'assistant': generated_text,
                'timestamp': time.time()
            })
            
            return generated_text
            
        except Exception as e:
            self.console.print(f"[red]生成回应时出错: {e}[/red]")
            return "抱歉，我在处理您的请求时遇到了问题。请稍后再试。"
    
    def chat_loop(self):
        """主聊天循环"""
        # 显示欢迎信息
        welcome_panel = Panel(
            Text("🚀 欢迎使用 Unlimited Agent！\n\n" +
                 "这是一个基于llama-cpp-python的无限制AI助手\n" +
                 "输入 'quit', 'exit' 或 'bye' 退出程序\n" +
                 "输入 'clear' 清空对话历史\n" +
                 "输入 'help' 查看帮助信息",
                 style="cyan"),
            title="Unlimited Agent v1.0",
            border_style="bright_blue"
        )
        self.console.print(welcome_panel)
        
        while True:
            try:
                # 获取用户输入
                user_input = Prompt.ask("\n[bold green]您[/bold green]").strip()
                
                # 处理特殊命令
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    self.console.print("[yellow]👋 再见！感谢使用 Unlimited Agent！[/yellow]")
                    break
                elif user_input.lower() == 'clear':
                    self.conversation_history.clear()
                    self.console.print("[green]✅ 对话历史已清空[/green]")
                    continue
                elif user_input.lower() == 'help':
                    self._show_help()
                    continue
                elif not user_input:
                    continue
                
                # 生成并显示回应
                self.console.print("[yellow]🤖 思考中...[/yellow]")
                response = self.generate_response(user_input)
                
                # 美化输出
                response_panel = Panel(
                    Text(response, style="white"),
                    title="🤖 Unlimited Agent",
                    border_style="bright_magenta"
                )
                self.console.print(response_panel)
                
            except KeyboardInterrupt:
                self.console.print("\n[yellow]👋 程序被用户中断，再见！[/yellow]")
                break
            except Exception as e:
                self.console.print(f"[red]❌ 发生错误: {e}[/red]")
    
    def _show_help(self):
        """显示帮助信息"""
        help_text = """
🔧 可用命令:
• quit/exit/bye - 退出程序
• clear - 清空对话历史
• help - 显示此帮助信息

💡 使用技巧:
• 可以进行多轮对话，我会记住上下文
• 支持中英文对话
• 可以询问任何问题，我会尽力回答
• 如果回答不满意，可以要求我重新回答

⚙️ 当前配置:
• 上下文长度: 4096 tokens
• 最大回应长度: 2048 tokens
• 温度: 0.7
• 对话历史保留: 最近10轮
"""
        
        help_panel = Panel(
            Text(help_text, style="cyan"),
            title="📖 帮助信息",
            border_style="bright_cyan"
        )
        self.console.print(help_panel)

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Unlimited Agent - 无限制AI助手")
    parser.add_argument("--model-path", type=str, help="本地模型文件路径")
    parser.add_argument("--model-repo", type=str, help="Hugging Face模型仓库ID")
    parser.add_argument("--model-filename", type=str, help="模型文件名")
    parser.add_argument("--temperature", type=float, default=0.7, help="生成温度 (0.0-1.0)")
    parser.add_argument("--max-tokens", type=int, default=2048, help="最大生成token数")
    
    args = parser.parse_args()
    
    try:
        # 创建Agent实例
        agent = UnlimitedAgent(
            model_path=args.model_path,
            model_repo=args.model_repo,
            model_filename=args.model_filename
        )
        
        # 更新配置
        if args.temperature:
            agent.model_config['temperature'] = args.temperature
        if args.max_tokens:
            agent.model_config['max_tokens'] = args.max_tokens
        
        # 开始聊天
        agent.chat_loop()
        
    except Exception as e:
        console.print(f"[red]❌ 启动失败: {e}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()