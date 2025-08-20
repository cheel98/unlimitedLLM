#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用OpenAI GPT 20B模型的示例
作者: Unlimited AI Team
版本: 1.0.0
"""

from unlimited_agent import UnlimitedAgent

def main():
    """
    使用指定的OpenAI GPT 20B模型创建Agent
    """
    print("🚀 正在初始化OpenAI GPT 20B无审查模型...")
    
    # 创建Agent实例，使用指定的模型
    agent = UnlimitedAgent(
        model_repo="DavidAU/OpenAi-GPT-oss-20b-abliterated-uncensored-NEO-Imatrix-gguf",
        model_filename="OpenAI-20B-NEO-CODE-DI-Uncensored-Q5_1.gguf",
        use_pretrained=True  # 使用from_pretrained方法
    )
    
    print("\n✅ 模型初始化完成！")
    print("\n📝 模型信息:")
    print("   - 仓库: DavidAU/OpenAi-GPT-oss-20b-abliterated-uncensored-NEO-Imatrix-gguf")
    print("   - 文件: OpenAI-20B-NEO-CODE-DI-Uncensored-Q5_1.gguf")
    print("   - 类型: 20B参数无审查模型")
    print("   - 特点: 支持代码生成和创意写作")
    
    # 启动聊天循环
    print("\n🎯 开始对话 (输入 'quit' 退出, 'help' 查看帮助):")
    agent.chat_loop()

if __name__ == "__main__":
    main()