# 模型使用指南

本文档详细介绍如何在Unlimited Agent中使用不同类型的模型。

## 支持的模型加载方式

### 1. 使用 `from_pretrained` 方法（推荐）

这是加载GGUF格式模型的推荐方式，特别适用于量化模型。

```python
from unlimited_agent import UnlimitedAgent

# 使用OpenAI GPT 20B无审查模型
agent = UnlimitedAgent(
    model_repo="DavidAU/OpenAi-GPT-oss-20b-abliterated-uncensored-NEO-Imatrix-gguf",
    model_filename="OpenAI-20B-NEO-CODE-DI-Uncensored-Q5_1.gguf",
    use_pretrained=True
)
```

### 2. 传统Hugging Face下载方式

适用于标准的Hugging Face模型。

```python
# 使用传统方式加载模型
agent = UnlimitedAgent(
    model_repo="microsoft/DialoGPT-medium",
    model_filename="pytorch_model.bin",
    use_pretrained=False  # 默认值
)
```

### 3. 本地模型文件

如果你已经下载了模型文件到本地。

```python
# 使用本地模型文件
agent = UnlimitedAgent(
    model_path="/path/to/your/model.gguf"
)
```

## 推荐模型列表

### 1. OpenAI GPT 20B 无审查模型（默认）
- **仓库**: `DavidAU/OpenAi-GPT-oss-20b-abliterated-uncensored-NEO-Imatrix-gguf`
- **文件**: `OpenAI-20B-NEO-CODE-DI-Uncensored-Q5_1.gguf`
- **特点**: 20B参数，无内容审查，支持代码生成
- **用法**: `use_pretrained=True`

### 2. Llama-2 7B 聊天模型
- **仓库**: `TheBloke/Llama-2-7B-Chat-GGML`
- **文件**: `llama-2-7b-chat.q4_0.bin`
- **特点**: 7B参数，专门优化对话
- **用法**: `use_pretrained=False`

### 3. 微软对话模型
- **仓库**: `microsoft/DialoGPT-medium`
- **文件**: `pytorch_model.bin`
- **特点**: 中等规模，快速响应
- **用法**: `use_pretrained=False`

## 模型配置参数

你可以通过修改 `model_config` 来调整模型行为：

```python
agent = UnlimitedAgent(
    model_repo="your_repo",
    model_filename="your_file.gguf",
    use_pretrained=True
)

# 修改模型配置
agent.model_config.update({
    'temperature': 0.8,      # 创造性（0.1-1.0）
    'top_p': 0.95,          # 核采样
    'top_k': 50,            # 顶k采样
    'max_tokens': 4096,     # 最大生成长度
    'n_gpu_layers': 32,     # GPU加速层数（如果支持）
})
```

## 使用示例

### 快速开始

```python
# 使用默认的OpenAI GPT 20B模型
from unlimited_agent import UnlimitedAgent

agent = UnlimitedAgent()  # 自动使用默认模型
agent.chat_loop()  # 开始对话
```

### 自定义模型

```python
# 使用你指定的模型
agent = UnlimitedAgent(
    model_repo="DavidAU/OpenAi-GPT-oss-20b-abliterated-uncensored-NEO-Imatrix-gguf",
    model_filename="OpenAI-20B-NEO-CODE-DI-Uncensored-Q5_1.gguf",
    use_pretrained=True
)

# 单次对话
response = agent.generate_response("你好，请介绍一下你自己")
print(response)

# 持续对话
agent.chat_loop()
```

### 编程接口使用

```python
# 在你的应用中集成
class MyApp:
    def __init__(self):
        self.agent = UnlimitedAgent(
            model_repo="DavidAU/OpenAi-GPT-oss-20b-abliterated-uncensored-NEO-Imatrix-gguf",
            model_filename="OpenAI-20B-NEO-CODE-DI-Uncensored-Q5_1.gguf",
            use_pretrained=True
        )
    
    def get_ai_response(self, user_input: str) -> str:
        return self.agent.generate_response(user_input)
    
    def clear_history(self):
        self.agent.conversation_history.clear()
```

## 故障排除

### 1. 模型加载失败
- 检查网络连接
- 确认模型仓库和文件名正确
- 检查磁盘空间是否足够

### 2. 内存不足
- 尝试使用更小的模型
- 减少 `n_ctx` 参数
- 启用GPU加速（设置 `n_gpu_layers`）

### 3. 响应速度慢
- 增加 `n_threads` 参数
- 使用GPU加速
- 选择量化程度更高的模型（如Q4_0而不是Q8_0）

## 注意事项

1. **首次使用**：模型会自动下载到 `./models` 目录，可能需要较长时间
2. **存储空间**：大型模型可能需要几GB到几十GB的存储空间
3. **系统要求**：建议至少8GB RAM，16GB或更多更佳
4. **GPU支持**：如果有NVIDIA GPU，可以设置 `n_gpu_layers` 来加速推理

## 更多信息

- 查看 `example_openai_model.py` 获取完整示例
- 运行 `python run.py --help` 查看命令行选项
- 访问 [llama-cpp-python文档](https://github.com/abetlen/llama-cpp-python) 了解更多配置选项