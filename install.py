#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安装脚本 - Unlimited Agent
处理依赖安装，特别是llama-cpp-python的复杂安装
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(cmd, check=True):
    """运行命令"""
    print(f"执行: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        if e.stderr:
            print(f"错误信息: {e.stderr}")
        return False

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ 错误: 需要Python 3.8或更高版本")
        print(f"当前版本: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python版本检查通过: {version.major}.{version.minor}.{version.micro}")
    return True

def install_basic_dependencies():
    """安装基础依赖"""
    print("\n📦 安装基础依赖...")
    basic_deps = [
        "huggingface-hub==0.19.4",
        "requests==2.31.0",
        "colorama==0.4.6",
        "python-dotenv==1.0.0",
        "rich==13.7.0"
    ]
    
    for dep in basic_deps:
        if not run_command(f"pip install {dep}"):
            print(f"❌ 安装 {dep} 失败")
            return False
    
    print("✅ 基础依赖安装完成")
    return True

def install_llama_cpp_python():
    """安装llama-cpp-python"""
    print("\n🦙 安装 llama-cpp-python...")
    
    # 检测系统架构
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    print(f"检测到系统: {system} {machine}")
    
    # 尝试不同的安装方法
    install_methods = []
    
    if system == "windows":
        # Windows预编译版本
        install_methods = [
            "pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu",
            "pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121",  # CUDA 12.1
            "pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu118",  # CUDA 11.8
            "pip install llama-cpp-python",  # 从源码编译
        ]
    elif system == "darwin":  # macOS
        install_methods = [
            "pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/metal",
            "pip install llama-cpp-python",
        ]
    else:  # Linux
        install_methods = [
            "pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu",
            "pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121",
            "pip install llama-cpp-python",
        ]
    
    for i, method in enumerate(install_methods, 1):
        print(f"\n尝试方法 {i}/{len(install_methods)}: {method}")
        if run_command(method, check=False):
            print("✅ llama-cpp-python 安装成功")
            return True
        print(f"❌ 方法 {i} 失败，尝试下一个...")
    
    print("❌ 所有安装方法都失败了")
    return False

def test_installation():
    """测试安装"""
    print("\n🧪 测试安装...")
    
    try:
        # 测试基础依赖
        import rich
        import huggingface_hub
        import requests
        import colorama
        print("✅ 基础依赖导入成功")
        
        # 测试llama-cpp-python
        try:
            import llama_cpp
            print("✅ llama-cpp-python 导入成功")
            return True
        except ImportError:
            print("⚠️ llama-cpp-python 导入失败，将使用演示模式")
            return True  # 仍然可以运行演示模式
            
    except ImportError as e:
        print(f"❌ 依赖导入失败: {e}")
        return False

def create_demo_mode_notice():
    """创建演示模式说明文件"""
    notice_content = """
# 演示模式说明

由于llama-cpp-python安装失败，Unlimited Agent将以演示模式运行。

## 演示模式特点：
- 不需要下载大型语言模型
- 提供预设的回复来演示界面和功能
- 可以体验完整的用户界面
- 所有功能都可以正常使用，只是回复是模拟的

## 如何启用完整功能：
1. 手动安装llama-cpp-python:
   ```
   pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
   ```

2. 或者安装支持CUDA的版本（如果有NVIDIA GPU）:
   ```
   pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121
   ```

3. 重新运行程序即可使用真实的AI模型

## 系统要求：
- Windows: 需要Visual Studio Build Tools
- macOS: 需要Xcode Command Line Tools
- Linux: 需要gcc和cmake
"""
    
    with open("DEMO_MODE.md", "w", encoding="utf-8") as f:
        f.write(notice_content)
    
    print("📝 已创建演示模式说明文件: DEMO_MODE.md")

def main():
    """主安装流程"""
    print("🚀 Unlimited Agent 安装程序")
    print("=" * 40)
    
    # 检查Python版本
    if not check_python_version():
        return False
    
    # 升级pip
    print("\n📦 升级pip...")
    run_command("python -m pip install --upgrade pip", check=False)
    
    # 安装基础依赖
    if not install_basic_dependencies():
        print("❌ 基础依赖安装失败")
        return False
    
    # 安装llama-cpp-python
    llama_cpp_success = install_llama_cpp_python()
    
    # 测试安装
    if not test_installation():
        print("❌ 安装测试失败")
        return False
    
    # 如果llama-cpp-python安装失败，创建演示模式说明
    if not llama_cpp_success:
        create_demo_mode_notice()
        print("\n⚠️ 注意: llama-cpp-python安装失败，程序将以演示模式运行")
        print("请查看 DEMO_MODE.md 了解如何启用完整功能")
    
    print("\n🎉 安装完成！")
    print("\n使用方法:")
    print("  python run.py          # 交互式启动")
    print("  python run.py --quick  # 快速启动")
    print("  start.bat              # Windows批处理启动")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ 安装失败")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️ 安装被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 安装过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)