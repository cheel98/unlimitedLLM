#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模型管理器 - Unlimited Agent
负责模型的下载、加载和管理
"""

import os
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

try:
    from huggingface_hub import hf_hub_download, list_repo_files
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
    from rich.table import Table
    from rich.panel import Panel
except ImportError as e:
    print(f"缺少依赖库: {e}")
    raise

from config import Config

@dataclass
class ModelInfo:
    """模型信息数据类"""
    name: str
    repo_id: str
    filename: str
    description: str
    size: str
    local_path: Optional[str] = None
    is_downloaded: bool = False
    checksum: Optional[str] = None

class ModelManager:
    """模型管理器类"""
    
    def __init__(self, models_dir: str = "./models"):
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(exist_ok=True)
        self.console = Console()
        self.model_registry_file = self.models_dir / "model_registry.json"
        self.model_registry = self._load_model_registry()
    
    def _load_model_registry(self) -> Dict:
        """加载模型注册表"""
        if self.model_registry_file.exists():
            try:
                with open(self.model_registry_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.console.print(f"[yellow]警告: 无法加载模型注册表: {e}[/yellow]")
        return {}
    
    def _save_model_registry(self):
        """保存模型注册表"""
        try:
            with open(self.model_registry_file, 'w', encoding='utf-8') as f:
                json.dump(self.model_registry, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.console.print(f"[red]错误: 无法保存模型注册表: {e}[/red]")
    
    def _calculate_file_checksum(self, file_path: Path) -> str:
        """计算文件校验和"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception:
            return ""
    
    def list_available_models(self) -> List[ModelInfo]:
        """列出所有可用模型"""
        models = []
        for model_config in Config.get_all_models():
            model_info = ModelInfo(
                name=model_config['name'],
                repo_id=model_config['repo_id'],
                filename=model_config['filename'],
                description=model_config['description'],
                size=model_config['size']
            )
            
            # 检查是否已下载
            local_path = self.models_dir / model_config['filename']
            if local_path.exists():
                model_info.local_path = str(local_path)
                model_info.is_downloaded = True
                model_info.checksum = self._calculate_file_checksum(local_path)
            
            models.append(model_info)
        
        return models
    
    def display_models_table(self):
        """显示模型表格"""
        models = self.list_available_models()
        
        table = Table(title="🤖 可用模型列表")
        table.add_column("名称", style="cyan", no_wrap=True)
        table.add_column("描述", style="white")
        table.add_column("大小", style="yellow")
        table.add_column("状态", style="green")
        table.add_column("推荐", style="magenta")
        
        for model in models:
            # 检查是否为推荐模型
            is_recommended = any(
                m['name'] == model.name and m.get('recommended', False) 
                for m in Config.get_all_models()
            )
            
            status = "✅ 已下载" if model.is_downloaded else "⬇️ 未下载"
            recommended = "⭐" if is_recommended else ""
            
            table.add_row(
                model.name,
                model.description,
                model.size,
                status,
                recommended
            )
        
        self.console.print(table)
    
    def download_model(self, model_name: str, force_redownload: bool = False) -> Optional[str]:
        """下载指定模型"""
        # 查找模型配置
        model_config = None
        for config in Config.get_all_models():
            if config['name'] == model_name:
                model_config = config
                break
        
        if not model_config:
            self.console.print(f"[red]错误: 未找到模型 '{model_name}'[/red]")
            return None
        
        local_path = self.models_dir / model_config['filename']
        
        # 检查是否已存在且不强制重新下载
        if local_path.exists() and not force_redownload:
            self.console.print(f"[green]模型 '{model_name}' 已存在: {local_path}[/green]")
            return str(local_path)
        
        try:
            self.console.print(f"[yellow]开始下载模型: {model_name}[/yellow]")
            self.console.print(f"[cyan]仓库: {model_config['repo_id']}[/cyan]")
            self.console.print(f"[cyan]文件: {model_config['filename']}[/cyan]")
            
            # 使用进度条下载
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                console=self.console
            ) as progress:
                task = progress.add_task(f"下载 {model_name}...", total=None)
                
                # 下载模型
                downloaded_path = hf_hub_download(
                    repo_id=model_config['repo_id'],
                    filename=model_config['filename'],
                    cache_dir=str(self.models_dir),
                    local_dir=str(self.models_dir),
                    local_dir_use_symlinks=False
                )
                
                progress.update(task, completed=True)
            
            # 更新模型注册表
            self.model_registry[model_name] = {
                'repo_id': model_config['repo_id'],
                'filename': model_config['filename'],
                'local_path': downloaded_path,
                'checksum': self._calculate_file_checksum(Path(downloaded_path)),
                'download_time': str(Path(downloaded_path).stat().st_mtime)
            }
            self._save_model_registry()
            
            self.console.print(f"[green]✅ 模型下载完成: {downloaded_path}[/green]")
            return downloaded_path
            
        except Exception as e:
            self.console.print(f"[red]❌ 模型下载失败: {e}[/red]")
            return None
    
    def delete_model(self, model_name: str) -> bool:
        """删除指定模型"""
        model_config = None
        for config in Config.get_all_models():
            if config['name'] == model_name:
                model_config = config
                break
        
        if not model_config:
            self.console.print(f"[red]错误: 未找到模型 '{model_name}'[/red]")
            return False
        
        local_path = self.models_dir / model_config['filename']
        
        if not local_path.exists():
            self.console.print(f"[yellow]模型 '{model_name}' 未下载，无需删除[/yellow]")
            return True
        
        try:
            local_path.unlink()
            
            # 从注册表中移除
            if model_name in self.model_registry:
                del self.model_registry[model_name]
                self._save_model_registry()
            
            self.console.print(f"[green]✅ 模型 '{model_name}' 已删除[/green]")
            return True
            
        except Exception as e:
            self.console.print(f"[red]❌ 删除模型失败: {e}[/red]")
            return False
    
    def get_model_path(self, model_name: str) -> Optional[str]:
        """获取模型本地路径"""
        model_config = None
        for config in Config.get_all_models():
            if config['name'] == model_name:
                model_config = config
                break
        
        if not model_config:
            return None
        
        local_path = self.models_dir / model_config['filename']
        return str(local_path) if local_path.exists() else None
    
    def verify_model_integrity(self, model_name: str) -> bool:
        """验证模型完整性"""
        local_path = self.get_model_path(model_name)
        if not local_path or not Path(local_path).exists():
            return False
        
        # 检查文件大小（简单验证）
        file_size = Path(local_path).stat().st_size
        if file_size < 1024 * 1024:  # 小于1MB可能有问题
            return False
        
        return True
    
    def get_storage_info(self) -> Dict[str, str]:
        """获取存储信息"""
        total_size = 0
        model_count = 0
        
        for model_file in self.models_dir.glob("*.bin"):
            if model_file.is_file():
                total_size += model_file.stat().st_size
                model_count += 1
        
        # 转换为人类可读格式
        def format_size(size_bytes):
            if size_bytes < 1024:
                return f"{size_bytes} B"
            elif size_bytes < 1024**2:
                return f"{size_bytes/1024:.1f} KB"
            elif size_bytes < 1024**3:
                return f"{size_bytes/(1024**2):.1f} MB"
            else:
                return f"{size_bytes/(1024**3):.1f} GB"
        
        return {
            'models_directory': str(self.models_dir),
            'total_models': str(model_count),
            'total_size': format_size(total_size),
            'total_size_bytes': str(total_size)
        }
    
    def cleanup_cache(self):
        """清理缓存文件"""
        cache_files = list(self.models_dir.glob("*.tmp")) + list(self.models_dir.glob("*.cache"))
        
        cleaned_count = 0
        for cache_file in cache_files:
            try:
                cache_file.unlink()
                cleaned_count += 1
            except Exception:
                pass
        
        if cleaned_count > 0:
            self.console.print(f"[green]✅ 清理了 {cleaned_count} 个缓存文件[/green]")
        else:
            self.console.print("[yellow]没有找到需要清理的缓存文件[/yellow]")

def main():
    """模型管理器命令行界面"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Unlimited Agent 模型管理器")
    parser.add_argument("action", choices=["list", "download", "delete", "info", "cleanup"],
                       help="要执行的操作")
    parser.add_argument("--model", type=str, help="模型名称")
    parser.add_argument("--force", action="store_true", help="强制重新下载")
    
    args = parser.parse_args()
    
    manager = ModelManager()
    
    if args.action == "list":
        manager.display_models_table()
    elif args.action == "download":
        if not args.model:
            print("错误: 请指定要下载的模型名称 (--model)")
            return
        manager.download_model(args.model, args.force)
    elif args.action == "delete":
        if not args.model:
            print("错误: 请指定要删除的模型名称 (--model)")
            return
        manager.delete_model(args.model)
    elif args.action == "info":
        info = manager.get_storage_info()
        console = Console()
        info_panel = Panel(
            f"模型目录: {info['models_directory']}\n"
            f"已下载模型: {info['total_models']}\n"
            f"总大小: {info['total_size']}",
            title="📊 存储信息",
            border_style="cyan"
        )
        console.print(info_panel)
    elif args.action == "cleanup":
        manager.cleanup_cache()

if __name__ == "__main__":
    main()