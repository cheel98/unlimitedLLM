from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
import os
from typing import List, Dict
from agent import get_agent

# 创建FastAPI应用
app = FastAPI(title="UnlimitedLLM Agent", description="基于GGUF模型的AI Agent")

# 设置模板目录
templates = Jinja2Templates(directory="templates")

# 创建静态文件目录（如果不存在）
static_dir = "static"
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

# 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

# 请求模型
class ChatRequest(BaseModel):
    message: str
    max_tokens: int = 512
    temperature: float = 0.7

class ChatResponse(BaseModel):
    response: str
    conversation_history: List[Dict[str, str]]

# 全局变量存储agent实例
agent_instance = None

def initialize_agent():
    """初始化agent"""
    global agent_instance
    if agent_instance is None:
        try:
            agent_instance = get_agent()
            print("Agent初始化成功")
        except Exception as e:
            print(f"Agent初始化失败: {e}")
            raise e
    return agent_instance

@app.on_event("startup")
async def startup_event():
    """应用启动时初始化agent"""
    try:
        initialize_agent()
        print("UnlimitedLLM Agent服务启动成功！")
    except Exception as e:
        print(f"模型加载失败，但服务将继续运行: {e}")
        print("将使用模拟模式提供基本功能")
        global agent_instance
        agent_instance = None  # 确保agent_instance为None，启用模拟模式

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """主页"""
    return templates.TemplateResponse("index.html", {"request": request})

# 模拟对话历史（当模型未加载时使用）
simulated_history = []

def get_simulated_response(message: str) -> str:
    """生成模拟回复（当模型未加载时使用）"""
    responses = [
        "很抱歉，当前模型正在加载中，这是一个模拟回复。请稍后再试。",
        "感谢您的消息！由于技术原因，我现在只能提供模拟回复。",
        "您好！我收到了您的消息，但目前模型暂时不可用。这是一个演示回复。",
        "抱歉，模型加载遇到了问题。不过您可以看到界面是正常工作的！",
        "这是一个模拟的AI回复。实际的模型需要正确配置后才能工作。"
    ]
    import random
    return random.choice(responses)

@app.post("/api/chat", response_model=ChatResponse)
async def chat_api(chat_request: ChatRequest):
    """聊天API接口"""
    try:
        if agent_instance is None:
            # 模拟模式：生成模拟回复
            response = get_simulated_response(chat_request.message)
            
            # 更新模拟对话历史
            simulated_history.append({"role": "user", "content": chat_request.message})
            simulated_history.append({"role": "assistant", "content": response})
            
            return ChatResponse(
                response=response,
                conversation_history=simulated_history.copy()
            )
        
        # 正常模式：使用实际模型
        response = agent_instance.generate_response(
            chat_request.message,
            max_tokens=chat_request.max_tokens,
            temperature=chat_request.temperature
        )
        
        # 获取对话历史
        history = agent_instance.get_conversation_history()
        
        return ChatResponse(
            response=response,
            conversation_history=history
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成回复失败: {str(e)}")

@app.post("/api/chat/web")
async def chat_web(request: Request, message: str = Form(...)):
    """Web表单聊天接口"""
    try:
        if agent_instance is None:
            # 模拟模式
            response = get_simulated_response(message)
            simulated_history.append({"role": "user", "content": message})
            simulated_history.append({"role": "assistant", "content": response})
            
            return templates.TemplateResponse("index.html", {
                "request": request,
                "response": response,
                "conversation_history": simulated_history.copy(),
                "user_message": message
            })
        
        # 正常模式
        response = agent_instance.generate_response(message)
        history = agent_instance.get_conversation_history()
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "response": response,
            "conversation_history": history,
            "user_message": message
        })
        
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": f"生成回复失败: {str(e)}"
        })

@app.post("/api/clear")
async def clear_history():
    """清空对话历史"""
    try:
        if agent_instance is None:
            # 模拟模式：清空模拟历史
            global simulated_history
            simulated_history = []
            return {"message": "对话历史已清空（模拟模式）"}
        
        # 正常模式
        agent_instance.clear_history()
        return {"message": "对话历史已清空"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"清空历史失败: {str(e)}")

@app.get("/api/history")
async def get_history():
    """获取对话历史"""
    try:
        if agent_instance is None:
            # 模拟模式：返回模拟历史
            return {"conversation_history": simulated_history.copy()}
        
        # 正常模式
        history = agent_instance.get_conversation_history()
        return {"conversation_history": history}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取历史失败: {str(e)}")

@app.get("/api/status")
async def get_status():
    """获取服务状态"""
    return {
        "status": "running",
        "agent_initialized": agent_instance is not None,
        "model_loaded": agent_instance is not None and agent_instance.llm is not None
    }

if __name__ == "__main__":
    # 运行服务器
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )