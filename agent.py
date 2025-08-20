import os
from typing import List, Dict, Any
from llama_cpp import Llama
import json

class UnlimitedLLMAgent:
    def __init__(self, model_path: str, n_ctx: int = 4096, n_threads: int = 4):
        """
        初始化UnlimitedLLM Agent
        
        Args:
            model_path: GGUF模型文件路径
            n_ctx: 上下文长度
            n_threads: 线程数
        """
        self.model_path = model_path
        self.n_ctx = n_ctx
        self.n_threads = n_threads
        self.llm = None
        self.conversation_history = []
        
        # 加载模型
        self._load_model()
    
    def _load_model(self):
        """加载GGUF模型"""
        try:
            print(f"正在加载模型: {self.model_path}")
            
            # 检查模型文件是否存在
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"模型文件不存在: {self.model_path}")
            
            # 尝试不同的参数组合来加载模型
            load_params = [
                # 第一次尝试：基本参数
                {
                    "model_path": self.model_path,
                    "n_ctx": self.n_ctx,
                    "n_threads": self.n_threads,
                    "verbose": False,
                    "n_gpu_layers": 0  # 先不使用GPU
                },
                # 第二次尝试：减少上下文长度
                {
                    "model_path": self.model_path,
                    "n_ctx": 2048,
                    "n_threads": 2,
                    "verbose": False,
                    "n_gpu_layers": 0
                },
                # 第三次尝试：最小配置
                {
                    "model_path": self.model_path,
                    "n_ctx": 512,
                    "n_threads": 1,
                    "verbose": True,
                    "n_gpu_layers": 0
                }
            ]
            
            for i, params in enumerate(load_params):
                try:
                    print(f"尝试加载模型 (配置 {i+1}/3): n_ctx={params['n_ctx']}, n_threads={params['n_threads']}")
                    self.llm = Llama(**params)
                    self.n_ctx = params['n_ctx']  # 更新实际使用的上下文长度
                    print(f"模型加载成功！使用配置: n_ctx={self.n_ctx}, n_threads={params['n_threads']}")
                    return
                except Exception as e:
                    print(f"配置 {i+1} 加载失败: {e}")
                    if i == len(load_params) - 1:  # 最后一次尝试
                        raise e
                    continue
                    
        except Exception as e:
            print(f"模型加载失败: {e}")
            print("请检查:")
            print("1. 模型文件是否存在且完整")
            print("2. 系统内存是否足够")
            print("3. llama-cpp-python版本是否兼容")
            raise e
    
    def generate_response(self, prompt: str, max_tokens: int = 512, temperature: float = 0.7) -> str:
        """
        生成回复
        
        Args:
            prompt: 输入提示
            max_tokens: 最大生成token数
            temperature: 温度参数
            
        Returns:
            生成的回复文本
        """
        try:
            # 构建完整的对话上下文
            full_prompt = self._build_conversation_prompt(prompt)
            
            # 生成回复
            response = self.llm(
                full_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                stop=["Human:", "Assistant:", "\n\n"],
                echo=False
            )
            
            generated_text = response['choices'][0]['text'].strip()
            
            # 更新对话历史
            self.conversation_history.append({"role": "user", "content": prompt})
            self.conversation_history.append({"role": "assistant", "content": generated_text})
            
            return generated_text
            
        except Exception as e:
            print(f"生成回复时出错: {e}")
            return f"抱歉，生成回复时出现错误: {str(e)}"
    
    def _build_conversation_prompt(self, current_prompt: str) -> str:
        """
        构建包含历史对话的完整提示
        
        Args:
            current_prompt: 当前用户输入
            
        Returns:
            完整的对话提示
        """
        # 系统提示
        system_prompt = "You are a helpful AI assistant. Please provide accurate and helpful responses.\n\n"
        
        # 构建对话历史
        conversation = system_prompt
        
        # 添加历史对话（保留最近的几轮对话以避免超出上下文长度）
        recent_history = self.conversation_history[-6:]  # 保留最近3轮对话
        
        for msg in recent_history:
            if msg["role"] == "user":
                conversation += f"Human: {msg['content']}\n"
            else:
                conversation += f"Assistant: {msg['content']}\n"
        
        # 添加当前提示
        conversation += f"Human: {current_prompt}\nAssistant: "
        
        return conversation
    
    def clear_history(self):
        """清空对话历史"""
        self.conversation_history = []
        print("对话历史已清空")
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """获取对话历史"""
        return self.conversation_history.copy()
    
    def save_conversation(self, filename: str):
        """保存对话历史到文件"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, ensure_ascii=False, indent=2)
            print(f"对话历史已保存到: {filename}")
        except Exception as e:
            print(f"保存对话历史失败: {e}")
    
    def load_conversation(self, filename: str):
        """从文件加载对话历史"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.conversation_history = json.load(f)
            print(f"对话历史已从 {filename} 加载")
        except Exception as e:
            print(f"加载对话历史失败: {e}")

# 创建全局agent实例
agent = None

def get_agent() -> UnlimitedLLMAgent:
    """获取agent实例"""
    global agent
    if agent is None:
        model_path = os.path.join(os.path.dirname(__file__), "model", "OpenAI-20B-NEO-CODE2-Plus-Uncensored-IQ4_NL.gguf")
        agent = UnlimitedLLMAgent(model_path)
    return agent

if __name__ == "__main__":
    # 测试代码
    try:
        test_agent = get_agent()
        print("Agent初始化成功！")
        
        # 测试对话
        response = test_agent.generate_response("你好，请介绍一下你自己。")
        print(f"回复: {response}")
        
    except Exception as e:
        print(f"测试失败: {e}")