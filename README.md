# 🚀 Unlimited Agent

基于 llama-cpp-python 和 Hugging Face 模型的无限制AI助手

## ✨ 特性

- 🔓 **无限制对话** - 不受传统AI的限制，可以自由对话
- 🧠 **智能推理** - 强大的逻辑分析和推理能力
- 💡 **创意思维** - 提供创新的解决方案和想法
- 🛠️ **本地运行** - 完全本地化，保护隐私，无需API密钥
- 🎯 **多种模式** - 支持默认、创意、技术、轻松等多种对话模式
- 📦 **模型管理** - 自动下载和管理多种开源大语言模型
- 🎨 **美观界面** - 基于Rich库的精美命令行界面
- 🤖 **多模型支持** - 支持GGUF格式模型和传统HuggingFace模型
- ⚡ **智能加载** - 支持from_pretrained方法，优化模型加载性能

## 🛠️ 安装

### 环境要求

- Python 3.8+
- Windows/Linux/macOS
- 至少 8GB RAM（推荐 16GB+）
- 至少 10GB 可用磁盘空间

### 快速安装

1. **克隆项目**
```bash
git clone <repository-url>
cd unlimited
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **运行程序**
```bash
python run.py
```

## 🚀 使用方法

### 方式一：交互式启动（推荐）

```bash
python run.py
```

程序会引导您：
1. 选择要使用的AI模型
2. 选择对话模式
3. 配置高级设置（可选）
4. 开始对话

### 方式二：快速启动

```bash
python run.py --quick
```

使用默认设置快速启动（演示模式）

### 方式三：直接启动主程序

```bash
# 使用本地模型
python unlimited_agent.py --model-path /path/to/your/model.bin

# 使用Hugging Face模型
python unlimited_agent.py --model-repo "TheBloke/Llama-2-7B-Chat-GGML" --model-filename "llama-2-7b-chat.q4_0.bin"
```

## 🤖 支持的模型

| 模型名称 | 大小 | 描述 | 推荐 |
|---------|------|------|------|
| **OpenAI GPT 20B** | ~12GB | 20B参数无审查模型，支持代码生成 | ⭐⭐⭐ |
| Llama-2-7B-Chat | 3.5GB | Meta的Llama-2聊天模型 | ⭐⭐ |
| Mistral-7B-Instruct | 3.5GB | Mistral AI的指令调优模型 | ⭐⭐ |
| OpenChat-3.5 | 3.5GB | OpenChat聊天模型 | ⭐ |
| CodeLlama-7B | 3.5GB | 专门用于代码生成 | ⭐ |
| Vicuna-7B | 3.5GB | 基于Llama的Vicuna模型 | - |

### 🌟 推荐模型：OpenAI GPT 20B 无审查模型

**默认模型**：`DavidAU/OpenAi-GPT-oss-20b-abliterated-uncensored-NEO-Imatrix-gguf`
- **文件**：`OpenAI-20B-NEO-CODE-DI-Uncensored-Q5_1.gguf`
- **参数量**：20B
- **特点**：无内容审查限制，支持代码生成和创意写作
- **适用场景**：编程、创意写作、技术问答、无限制对话

#### 快速使用示例

```python
from unlimited_agent import UnlimitedAgent

# 使用默认的OpenAI GPT 20B模型
agent = UnlimitedAgent()
agent.chat_loop()

# 或者显式指定模型
agent = UnlimitedAgent(
    model_repo="DavidAU/OpenAi-GPT-oss-20b-abliterated-uncensored-NEO-Imatrix-gguf",
    model_filename="OpenAI-20B-NEO-CODE-DI-Uncensored-Q5_1.gguf",
    use_pretrained=True
)
```

#### 运行示例脚本

```bash
python example_openai_model.py
```

## 🎭 对话模式

- **默认模式** - 平衡的AI助手，适合大多数场景
- **创意模式** - 专注于创意思考、写作和创新
- **技术模式** - 专业的技术问题解答和编程帮助
- **轻松模式** - 友好轻松的日常对话

## 📋 模型管理

### 查看可用模型
```bash
python model_manager.py list
```

### 下载模型
```bash
python model_manager.py download --model "Llama-2-7B-Chat"
```

### 删除模型
```bash
python model_manager.py delete --model "Llama-2-7B-Chat"
```

### 查看存储信息
```bash
python model_manager.py info
```

### 清理缓存
```bash
python model_manager.py cleanup
```

## ⚙️ 配置选项

### 模型参数

- `temperature` (0.0-1.0) - 生成随机性，越高越随机
- `max_tokens` (128-4096) - 最大生成长度
- `top_p` (0.0-1.0) - 核采样参数
- `top_k` (1-100) - Top-K采样参数
- `repeat_penalty` (1.0-1.5) - 重复惩罚

### 系统参数

- `n_ctx` (512-8192) - 上下文窗口大小
- `n_threads` (1-16) - CPU线程数
- `n_gpu_layers` (0-50) - GPU加速层数（需要CUDA支持）

## 💬 使用示例

### 基本对话
```
您: 你好，请介绍一下自己
🤖 Unlimited Agent: 你好！我是Unlimited Agent，一个基于开源大语言模型的AI助手...
```

### 创意写作
```
您: 帮我写一个科幻小说的开头
🤖 Unlimited Agent: 2087年，当最后一颗星星从地球的夜空中消失时...
```

### 技术问题
```
您: 如何用Python实现快速排序？
🤖 Unlimited Agent: 快速排序是一种高效的排序算法，以下是Python实现...
```

## 🔧 高级功能

### 自定义系统提示词

编辑 `config.py` 中的 `SYSTEM_PROMPTS` 来自定义AI的行为模式。

### 添加新模型

在 `config.py` 的 `RECOMMENDED_MODELS` 中添加新的模型配置：

```python
{
    "name": "Your-Model-Name",
    "repo_id": "huggingface/model-repo",
    "filename": "model-file.bin",
    "description": "模型描述",
    "size": "文件大小",
    "recommended": True
}
```

### 环境变量配置

创建 `.env` 文件来配置环境变量：

```env
HUGGINGFACE_TOKEN=your_hf_token_here
CUDA_VISIBLE_DEVICES=0
DEBUG=false
```

## 🐛 故障排除

### 常见问题

**Q: 模型下载失败**
A: 检查网络连接，或尝试使用代理。某些模型可能需要Hugging Face账户。

**Q: 内存不足**
A: 尝试使用更小的模型，或调整 `n_ctx` 参数。

**Q: 生成速度慢**
A: 增加 `n_threads` 参数，或考虑使用GPU加速（需要CUDA）。

**Q: 回答质量不佳**
A: 调整 `temperature` 和 `top_p` 参数，或尝试不同的模型。

### 日志和调试

## 📚 详细文档

- **[模型使用指南](MODEL_USAGE.md)** - 详细的模型加载和配置说明
- **[示例脚本](example_openai_model.py)** - OpenAI GPT 20B模型使用示例
- **[环境配置](.env.example)** - 环境变量配置模板

## 🔧 高级用法

### 自定义模型配置

```python
from unlimited_agent import UnlimitedAgent

agent = UnlimitedAgent(
    model_repo="DavidAU/OpenAi-GPT-oss-20b-abliterated-uncensored-NEO-Imatrix-gguf",
    model_filename="OpenAI-20B-NEO-CODE-DI-Uncensored-Q5_1.gguf",
    use_pretrained=True
)

# 自定义模型参数
agent.model_config.update({
    'temperature': 0.8,      # 创造性
    'top_p': 0.95,          # 核采样
    'max_tokens': 4096,     # 最大生成长度
    'n_gpu_layers': 32,     # GPU加速（如果支持）
})
```

### 编程接口集成

```python
# 在你的应用中使用
class MyAIApp:
    def __init__(self):
        self.agent = UnlimitedAgent(use_pretrained=True)
    
    def get_response(self, user_input: str) -> str:
        return self.agent.generate_response(user_input)
    
    def clear_history(self):
        self.agent.conversation_history.clear()
```

启用调试模式：
```bash
DEBUG=true python run.py
```

## 📄 许可证

MIT License - 详见 LICENSE 文件

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 支持

如果您遇到问题或有建议，请：

1. 查看本README的故障排除部分
2. 搜索已有的Issues
3. 创建新的Issue描述问题

## 🙏 致谢

- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) - 核心推理引擎
- [Hugging Face](https://huggingface.co/) - 模型托管平台
- [Rich](https://github.com/Textualize/rich) - 美观的命令行界面
- 所有开源模型的作者和贡献者

---

**🚀 开始您的无限制AI之旅吧！**