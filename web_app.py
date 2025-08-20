#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unlimited Agent Web应用
作者: Unlimited AI Team
版本: 1.0.0
"""

import os
import sys
import json
import uuid
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path

try:
    from flask import Flask, render_template, request, jsonify, session, send_from_directory
    from flask_cors import CORS
except ImportError:
    print("❌ 缺少Web依赖库，请安装: pip install flask flask-cors")
    sys.exit(1)

import traceback
from web_config import config
from unlimited_agent import UnlimitedAgent

class WebAgent:
    """Web版AI Agent"""
    
    def __init__(self):
        """初始化Web Agent"""
        self.sessions: Dict[str, Dict] = {}  # 存储用户会话
        self.agent = None
        self._init_agent()
    
    def _init_agent(self):
        """初始化AI Agent"""
        try:
            model_config = config.get_model_config()
            self.agent = UnlimitedAgent(
                model_repo=model_config['model_repo'],
                model_filename=model_config['model_filename'],
                use_pretrained=model_config['use_pretrained']
            )
            # 更新模型配置
            self.agent.model_config.update(model_config['model_config'])
            print(f"✅ AI Agent初始化成功: {model_config['model_name']}")
        except Exception as e:
            print(f"⚠️ AI Agent初始化失败: {e}")
            print("将使用演示模式")
            self.agent = None
    
    def get_session(self, session_id: str) -> Dict:
        """获取或创建用户会话"""
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                'id': session_id,
                'created_at': datetime.now().isoformat(),
                'messages': [],
                'model_info': config.get_model_config()
            }
        return self.sessions[session_id]
    
    def add_message(self, session_id: str, role: str, content: str) -> Dict:
        """添加消息到会话"""
        session_data = self.get_session(session_id)
        message = {
            'id': str(uuid.uuid4()),
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        }
        session_data['messages'].append(message)
        
        # 限制历史长度
        if len(session_data['messages']) > config.MAX_HISTORY_LENGTH * 2:
            session_data['messages'] = session_data['messages'][-config.MAX_HISTORY_LENGTH:]
        
        return message
    
    def generate_response(self, session_id: str, user_input: str) -> str:
        """生成AI回复"""
        if self.agent and self.agent.llm:
            # 使用真实模型
            try:
                # 设置会话历史
                session_data = self.get_session(session_id)
                self.agent.conversation_history = [
                    {'role': msg['role'], 'content': msg['content']} 
                    for msg in session_data['messages'][-10:]  # 只保留最近10条消息
                ]
                return self.agent.generate_response(user_input)
            except Exception as e:
                return f"抱歉，生成回复时出现错误: {str(e)}"
        else:
            # 演示模式
            return f"[演示模式] 您说: \"{user_input}\"。这是一个模拟回复，实际使用需要安装llama-cpp-python并配置模型。"

# 创建Flask应用
app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = config.SECRET_KEY
CORS(app)  # 启用跨域支持

# 创建Web Agent实例
web_agent = WebAgent()

@app.route('/')
def index():
    """主页"""
    try:
        return render_template('index.html', 
                             config=config.get_model_config(),
                             theme=config.THEME)
    except Exception as e:
        return f"模板渲染错误: {str(e)}", 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """聊天API"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': '缺少消息内容'}), 400
        
        user_message = data['message'].strip()
        if not user_message:
            return jsonify({'error': '消息不能为空'}), 400
        
        # 获取或创建会话ID
        session_id = session.get('session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
            session['session_id'] = session_id
        
        # 添加用户消息
        user_msg = web_agent.add_message(session_id, 'user', user_message)
        
        # 生成AI回复
        ai_response = web_agent.generate_response(session_id, user_message)
        ai_msg = web_agent.add_message(session_id, 'assistant', ai_response)
        
        return jsonify({
            'success': True,
            'user_message': user_msg,
            'ai_message': ai_msg,
            'session_id': session_id
        })
    
    except Exception as e:
        print(f"聊天API错误: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500

@app.route('/api/history')
def get_history():
    """获取聊天历史"""
    try:
        session_id = session.get('session_id')
        if not session_id:
            return jsonify({'messages': []})
        
        session_data = web_agent.get_session(session_id)
        return jsonify({
            'messages': session_data['messages'],
            'session_info': {
                'id': session_data['id'],
                'created_at': session_data['created_at'],
                'model_info': session_data['model_info']
            }
        })
    
    except Exception as e:
        return jsonify({'error': f'获取历史失败: {str(e)}'}), 500

@app.route('/api/clear', methods=['POST'])
def clear_history():
    """清空聊天历史"""
    try:
        session_id = session.get('session_id')
        if session_id and session_id in web_agent.sessions:
            web_agent.sessions[session_id]['messages'] = []
        
        return jsonify({'success': True, 'message': '聊天历史已清空'})
    
    except Exception as e:
        return jsonify({'error': f'清空历史失败: {str(e)}'}), 500

@app.route('/api/config')
def get_config():
    """获取配置信息"""
    try:
        return jsonify({
            'model_config': config.get_model_config(),
            'theme': config.THEME,
            'max_history': config.MAX_HISTORY_LENGTH,
            'has_model': web_agent.agent is not None and web_agent.agent.llm is not None
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sessions')
def get_sessions():
    """获取所有会话列表"""
    sessions_info = []
    for sid, session_data in web_agent.sessions.items():
        sessions_info.append({
            'id': sid,
            'created_at': session_data['created_at'],
            'message_count': len(session_data['messages']),
            'last_message': session_data['messages'][-1]['content'][:50] + '...' 
                          if session_data['messages'] else '无消息'
        })
    
    return jsonify({'sessions': sessions_info})

# 静态文件路由
@app.route('/static/<path:filename>')
def static_files(filename):
    """提供静态文件"""
    return send_from_directory('static', filename)

@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({'error': '页面未找到'}), 404

@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    return jsonify({'error': '服务器内部错误'}), 500

def main():
    """启动Web应用"""
    print("🚀 启动Unlimited Agent Web应用...")
    print(f"📊 配置信息:")
    print(config)
    print(f"\n🌐 访问地址: http://{config.WEB_HOST}:{config.WEB_PORT}")
    print("按 Ctrl+C 停止服务器")
    
    try:
        app.run(
            host=config.WEB_HOST,
            port=config.WEB_PORT,
            debug=config.WEB_DEBUG,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print(traceback.format_exc())

if __name__ == '__main__':
    main()