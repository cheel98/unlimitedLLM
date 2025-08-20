# UnlimitedLLM Agent

基于GGUF模型的智能对话Agent，提供简洁美观的Web界面。

## 功能特性

- 🤖 支持GGUF格式的大语言模型
- 💬 实时对话交互
- 🌐 现代化Web界面
- 📝 对话历史管理
- 🚀 FastAPI后端架构
- 📱 响应式设计，支持移动端

## 项目结构

```
unlimitedLLM/
├── agent.py              # Agent核心逻辑
├── app.py                # FastAPI Web服务器
├── requirements.txt      # Python依赖
├── README.md            # 项目说明
├── model/               # 模型文件目录
│   └── OpenAI-20B-NEO-CODE2-Plus-Uncensored-IQ4_NL.gguf
└── templates/           # HTML模板
    └── index.html       # 主页面模板
```

## 安装和运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动服务

```bash
python app.py
```

或者使用uvicorn直接启动：

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### 3. 访问界面

打开浏览器访问：http://localhost:8000

## API接口

### 聊天接口

**POST** `/api/chat`

请求体：
```json
{
  "message": "你好",
  "max_tokens": 512,
  "temperature": 0.7
}
```

响应：
```json
{
  "response": "你好！我是AI助手...",
  "conversation_history": [
    {"role": "user", "content": "你好"},
    {"role": "assistant", "content": "你好！我是AI助手..."}
  ]
}
```

### 其他接口

- **POST** `/api/clear` - 清空对话历史
- **GET** `/api/history` - 获取对话历史
- **GET** `/api/status` - 获取服务状态

## 配置说明

### Agent配置

在 `agent.py` 中可以调整以下参数：

- `n_ctx`: 上下文长度（默认4096）
- `n_threads`: 线程数（默认4）
- `max_tokens`: 最大生成token数（默认512）
- `temperature`: 温度参数（默认0.7）

### 模型路径

模型文件路径在 `agent.py` 的 `get_agent()` 函数中配置：

```python
model_path = os.path.join(os.path.dirname(__file__), "model", "OpenAI-20B-NEO-CODE2-Plus-Uncensored-IQ4_NL.gguf")
```

## 使用说明

1. **开始对话**：在输入框中输入消息，按回车或点击发送按钮
2. **清空历史**：点击右上角的"清空对话"按钮
3. **多行输入**：按Shift+Enter可以换行
4. **移动端**：界面支持响应式设计，在手机上也能正常使用

## 技术栈

- **后端**：FastAPI + Python
- **AI模型**：llama-cpp-python
- **前端**：HTML + CSS + JavaScript
- **模板引擎**：Jinja2

## 注意事项

1. 首次启动时需要加载模型，可能需要几分钟时间
2. 模型文件较大，确保有足够的内存和存储空间
3. 生成回复的速度取决于硬件配置和模型大小
4. 建议在有GPU的环境中运行以获得更好的性能

## 故障排除

### 模型加载失败
- 检查模型文件路径是否正确
- 确保有足够的内存
- 检查llama-cpp-python是否正确安装

### 服务启动失败
- 检查端口8000是否被占用
- 确保所有依赖都已正确安装
- 查看控制台错误信息

## 许可证

本项目仅供学习和研究使用。