#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本 - Unlimited Agent
验证所有功能是否正常工作
"""

import sys
import os
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
except ImportError:
    print("请先运行: python install.py")
    sys.exit(1)

def test_imports():
    """测试导入"""
    console = Console()
    console.print("[bold cyan]🧪 测试模块导入...[/bold cyan]")
    
    results = []
    
    # 测试基础模块
    modules_to_test = [
        ('config', 'Config'),
        ('model_manager', 'ModelManager'),
        ('unlimited_agent', 'UnlimitedAgent'),
        ('run', 'AgentLauncher')
    ]
    
    for module_name, class_name in modules_to_test:
        try:
            module = __import__(module_name)
            if hasattr(module, class_name):
                results.append((module_name, class_name, "✅ 成功", "green"))
            else:
                results.append((module_name, class_name, "❌ 类不存在", "red"))
        except ImportError as e:
            results.append((module_name, class_name, f"❌ 导入失败: {e}", "red"))
        except Exception as e:
            results.append((module_name, class_name, f"❌ 错误: {e}", "red"))
    
    # 显示结果表格
    table = Table(title="模块导入测试结果")
    table.add_column("模块", style="cyan")
    table.add_column("类", style="yellow")
    table.add_column("状态", style="white")
    
    for module_name, class_name, status, color in results:
        table.add_row(module_name, class_name, f"[{color}]{status}[/{color}]")
    
    console.print(table)
    
    # 返回是否所有测试都通过
    return all("成功" in result[2] for result in results)

def test_config():
    """测试配置"""
    console = Console()
    console.print("\n[bold cyan]⚙️ 测试配置模块...[/bold cyan]")
    
    try:
        from config import Config, EnvConfig
        
        # 测试获取模型配置
        model_config = Config.get_model_config()
        console.print(f"[green]✅ 默认模型配置: {len(model_config)} 个参数[/green]")
        
        # 测试获取推荐模型
        recommended_models = Config.get_recommended_models()
        console.print(f"[green]✅ 推荐模型: {len(recommended_models)} 个[/green]")
        
        # 测试获取系统提示词
        system_prompt = Config.get_system_prompt()
        console.print(f"[green]✅ 系统提示词长度: {len(system_prompt)} 字符[/green]")
        
        # 测试目录创建
        Config.ensure_directories()
        console.print("[green]✅ 目录创建成功[/green]")
        
        return True
        
    except Exception as e:
        console.print(f"[red]❌ 配置测试失败: {e}[/red]")
        return False

def test_model_manager():
    """测试模型管理器"""
    console = Console()
    console.print("\n[bold cyan]🤖 测试模型管理器...[/bold cyan]")
    
    try:
        from model_manager import ModelManager
        
        manager = ModelManager()
        
        # 测试列出可用模型
        models = manager.list_available_models()
        console.print(f"[green]✅ 可用模型: {len(models)} 个[/green]")
        
        # 测试存储信息
        storage_info = manager.get_storage_info()
        console.print(f"[green]✅ 存储信息: {storage_info['total_models']} 个模型[/green]")
        
        return True
        
    except Exception as e:
        console.print(f"[red]❌ 模型管理器测试失败: {e}[/red]")
        return False

def test_agent():
    """测试Agent"""
    console = Console()
    console.print("\n[bold cyan]🚀 测试Agent...[/bold cyan]")
    
    try:
        from unlimited_agent import UnlimitedAgent
        
        # 创建Agent实例（演示模式）
        agent = UnlimitedAgent()
        console.print("[green]✅ Agent创建成功[/green]")
        
        # 测试生成回应
        response = agent.generate_response("你好")
        console.print(f"[green]✅ 生成回应: {len(response)} 字符[/green]")
        console.print(f"[cyan]回应内容: {response[:100]}...[/cyan]")
        
        return True
        
    except Exception as e:
        console.print(f"[red]❌ Agent测试失败: {e}[/red]")
        return False

def test_launcher():
    """测试启动器"""
    console = Console()
    console.print("\n[bold cyan]🚀 测试启动器...[/bold cyan]")
    
    try:
        from run import AgentLauncher
        
        launcher = AgentLauncher()
        console.print("[green]✅ 启动器创建成功[/green]")
        
        return True
        
    except Exception as e:
        console.print(f"[red]❌ 启动器测试失败: {e}[/red]")
        return False

def test_file_structure():
    """测试文件结构"""
    console = Console()
    console.print("\n[bold cyan]📁 测试文件结构...[/bold cyan]")
    
    required_files = [
        'unlimited_agent.py',
        'config.py',
        'model_manager.py',
        'run.py',
        'install.py',
        'requirements.txt',
        'README.md',
        'start.bat',
        '.env.example'
    ]
    
    missing_files = []
    for file_name in required_files:
        if not Path(file_name).exists():
            missing_files.append(file_name)
    
    if missing_files:
        console.print(f"[red]❌ 缺少文件: {', '.join(missing_files)}[/red]")
        return False
    else:
        console.print(f"[green]✅ 所有必需文件都存在 ({len(required_files)} 个)[/green]")
        return True

def main():
    """主测试函数"""
    console = Console()
    
    # 显示测试开始
    welcome_panel = Panel(
        "🧪 Unlimited Agent 功能测试\n\n"
        "这个脚本将测试所有核心功能是否正常工作",
        title="测试开始",
        border_style="bright_blue"
    )
    console.print(welcome_panel)
    
    # 运行所有测试
    tests = [
        ("文件结构", test_file_structure),
        ("模块导入", test_imports),
        ("配置模块", test_config),
        ("模型管理器", test_model_manager),
        ("Agent核心", test_agent),
        ("启动器", test_launcher)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            console.print(f"[red]❌ {test_name} 测试异常: {e}[/red]")
            results.append((test_name, False))
    
    # 显示测试结果摘要
    console.print("\n[bold cyan]📊 测试结果摘要[/bold cyan]")
    
    summary_table = Table(title="测试结果")
    summary_table.add_column("测试项目", style="cyan")
    summary_table.add_column("结果", style="white")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        if result:
            summary_table.add_row(test_name, "[green]✅ 通过[/green]")
            passed += 1
        else:
            summary_table.add_row(test_name, "[red]❌ 失败[/red]")
    
    console.print(summary_table)
    
    # 显示最终结果
    if passed == total:
        result_panel = Panel(
            f"🎉 所有测试通过！({passed}/{total})\n\n"
            "Unlimited Agent 已准备就绪！\n\n"
            "使用方法:\n"
            "• python run.py (交互式启动)\n"
            "• python run.py --quick (快速启动)\n"
            "• start.bat (Windows批处理)",
            title="✅ 测试成功",
            border_style="bright_green"
        )
    else:
        result_panel = Panel(
            f"⚠️ 部分测试失败 ({passed}/{total})\n\n"
            "请检查上述错误信息并修复问题",
            title="❌ 测试失败",
            border_style="bright_red"
        )
    
    console.print(result_panel)
    
    return passed == total

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)