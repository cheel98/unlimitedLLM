#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速启动脚本 - Unlimited Agent
提供简化的启动方式和交互式配置
"""

import os
import sys
import json
from pathlib import Path

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    from rich.text import Text
except ImportError:
    print("正在安装必要的依赖...")
    os.system("pip install rich")
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    from rich.text import Text

from config import Config
from model_manager import ModelManager
from unlimited_agent import UnlimitedAgent

class AgentLauncher:
    """Agent启动器"""
    
    def __init__(self):
        self.console = Console()
        self.model_manager = ModelManager()
        Config.ensure_directories()
    
    def show_welcome(self):
        """显示欢迎界面"""
        welcome_text = Text()
        welcome_text.append("🚀 欢迎使用 Unlimited Agent!\n\n", style="bold cyan")
        welcome_text.append("这是一个基于 llama-cpp-python 的无限制AI助手\n", style="white")
        welcome_text.append("支持多种开源大语言模型，无需API密钥\n\n", style="white")
        welcome_text.append("特性:\n", style="bold yellow")
        welcome_text.append("• 🔓 无限制对话 - 不受传统AI限制\n", style="green")
        welcome_text.append("• 🧠 智能推理 - 强大的逻辑分析能力\n", style="green")
        welcome_text.append("• 💡 创意思维 - 提供创新解决方案\n", style="green")
        welcome_text.append("• 🛠️ 本地运行 - 保护隐私，无需联网\n", style="green")
        welcome_text.append("• 🎯 多模式 - 支持不同的对话风格\n", style="green")
        
        panel = Panel(
            welcome_text,
            title="Unlimited Agent v1.0",
            border_style="bright_blue",
            padding=(1, 2)
        )
        self.console.print(panel)
    
    def check_dependencies(self) -> bool:
        """检查依赖"""
        try:
            import llama_cpp
            import huggingface_hub
            return True
        except ImportError as e:
            self.console.print(f"[red]❌ 缺少依赖: {e}[/red]")
            if Confirm.ask("是否现在安装依赖?"):
                self.console.print("[yellow]正在安装依赖...[/yellow]")
                os.system("pip install -r requirements.txt")
                return True
            return False
    
    def select_model(self) -> tuple:
        """选择模型"""
        self.console.print("\n[bold cyan]📋 模型选择[/bold cyan]")
        
        # 显示可用模型
        models = Config.get_all_models()
        
        table = Table(title="可用模型")
        table.add_column("序号", style="cyan", width=6)
        table.add_column("名称", style="yellow")
        table.add_column("描述", style="white")
        table.add_column("大小", style="green")
        table.add_column("推荐", style="magenta")
        table.add_column("状态", style="blue")
        
        for i, model in enumerate(models, 1):
            recommended = "⭐" if model.get('recommended', False) else ""
            
            # 检查是否已下载
            local_path = self.model_manager.get_model_path(model['name'])
            status = "✅ 已下载" if local_path else "⬇️ 未下载"
            
            table.add_row(
                str(i),
                model['name'],
                model['description'],
                model['size'],
                recommended,
                status
            )
        
        self.console.print(table)
        
        # 用户选择
        while True:
            try:
                choice = Prompt.ask(
                    "\n请选择模型 (输入序号)",
                    default="1"
                )
                
                if choice.lower() == 'q':
                    return None, None
                
                model_index = int(choice) - 1
                if 0 <= model_index < len(models):
                    selected_model = models[model_index]
                    break
                else:
                    self.console.print("[red]无效选择，请重新输入[/red]")
            except ValueError:
                self.console.print("[red]请输入有效的数字[/red]")
        
        # 检查是否需要下载
        model_name = selected_model['name']
        local_path = self.model_manager.get_model_path(model_name)
        
        if not local_path:
            self.console.print(f"\n[yellow]模型 '{model_name}' 未下载[/yellow]")
            if Confirm.ask("是否现在下载?", default=True):
                local_path = self.model_manager.download_model(model_name)
                if not local_path:
                    self.console.print("[red]模型下载失败[/red]")
                    return None, None
            else:
                self.console.print("[yellow]将使用演示模式[/yellow]")
                return None, None
        
        return selected_model, local_path
    
    def select_mode(self) -> str:
        """选择对话模式"""
        self.console.print("\n[bold cyan]🎭 对话模式选择[/bold cyan]")
        
        modes = {
            '1': ('default', '默认模式', '平衡的AI助手，适合大多数场景'),
            '2': ('creative', '创意模式', '专注于创意思考和创新'),
            '3': ('technical', '技术模式', '专业的技术问题解答'),
            '4': ('casual', '轻松模式', '友好轻松的日常对话')
        }
        
        table = Table(title="对话模式")
        table.add_column("序号", style="cyan", width=6)
        table.add_column("模式", style="yellow")
        table.add_column("描述", style="white")
        
        for key, (mode_key, mode_name, description) in modes.items():
            table.add_row(key, mode_name, description)
        
        self.console.print(table)
        
        while True:
            choice = Prompt.ask("请选择对话模式", default="1")
            if choice in modes:
                return modes[choice][0]
            else:
                self.console.print("[red]无效选择，请重新输入[/red]")
    
    def configure_settings(self) -> dict:
        """配置设置"""
        self.console.print("\n[bold cyan]⚙️ 高级设置 (可选)[/bold cyan]")
        
        if not Confirm.ask("是否要自定义高级设置?", default=False):
            return Config.get_model_config()
        
        settings = {}
        
        # 温度设置
        temp = Prompt.ask(
            "生成温度 (0.0-1.0, 越高越随机)",
            default="0.7"
        )
        try:
            settings['temperature'] = float(temp)
        except ValueError:
            settings['temperature'] = 0.7
        
        # 最大token数
        max_tokens = Prompt.ask(
            "最大生成token数 (128-4096)",
            default="2048"
        )
        try:
            settings['max_tokens'] = int(max_tokens)
        except ValueError:
            settings['max_tokens'] = 2048
        
        # 上下文长度
        n_ctx = Prompt.ask(
            "上下文长度 (512-8192)",
            default="4096"
        )
        try:
            settings['n_ctx'] = int(n_ctx)
        except ValueError:
            settings['n_ctx'] = 4096
        
        return Config.get_model_config(**settings)
    
    def run(self):
        """运行启动器"""
        # 显示欢迎界面
        self.show_welcome()
        
        # 检查依赖
        if not self.check_dependencies():
            self.console.print("[red]依赖检查失败，程序退出[/red]")
            return
        
        try:
            # 选择模型
            selected_model, model_path = self.select_model()
            
            # 选择对话模式
            mode = self.select_mode()
            
            # 配置设置
            model_config = self.configure_settings()
            
            # 创建并启动Agent
            self.console.print("\n[green]🚀 正在启动 Unlimited Agent...[/green]")
            
            if model_path:
                agent = UnlimitedAgent(model_path=model_path)
            else:
                agent = UnlimitedAgent()  # 演示模式
            
            # 设置系统提示词
            agent.system_prompt = Config.get_system_prompt(mode)
            
            # 更新模型配置
            agent.model_config.update(model_config)
            
            # 开始聊天
            agent.chat_loop()
            
        except KeyboardInterrupt:
            self.console.print("\n[yellow]👋 程序被用户中断[/yellow]")
        except Exception as e:
            self.console.print(f"[red]❌ 启动失败: {e}[/red]")
            import traceback
            traceback.print_exc()

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Unlimited Agent 启动器")
    parser.add_argument("--quick", action="store_true", help="快速启动（使用默认设置）")
    parser.add_argument("--model", type=str, help="指定模型名称")
    parser.add_argument("--mode", type=str, choices=['default', 'creative', 'technical', 'casual'],
                       default='default', help="指定对话模式")
    
    args = parser.parse_args()
    
    if args.quick:
        # 快速启动模式
        console = Console()
        console.print("[green]🚀 快速启动模式[/green]")
        
        try:
            agent = UnlimitedAgent()
            agent.system_prompt = Config.get_system_prompt(args.mode)
            agent.chat_loop()
        except Exception as e:
            console.print(f"[red]启动失败: {e}[/red]")
    else:
        # 交互式启动
        launcher = AgentLauncher()
        launcher.run()

if __name__ == "__main__":
    main()