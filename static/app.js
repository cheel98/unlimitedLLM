// Unlimited Agent - 前端交互脚本

class ChatApp {
    constructor() {
        this.isLoading = false;
        this.messageCount = 0;
        this.currentTheme = document.body.getAttribute('data-theme') || 'light';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadChatHistory();
        this.checkStatus();
        this.updateThemeIcon();
    }

    setupEventListeners() {
        const input = document.getElementById('messageInput');
        const sendBtn = document.getElementById('sendBtn');
        
        // 回车发送消息
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // 自动调整输入框高度
        input.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 120) + 'px';
        });

        // 发送按钮点击
        sendBtn.addEventListener('click', () => this.sendMessage());
    }

    async sendMessage() {
        const input = document.getElementById('messageInput');
        const message = input.value.trim();
        
        if (!message || this.isLoading) return;
        
        this.isLoading = true;
        input.value = '';
        input.style.height = 'auto';
        this.updateSendButton(true);
        
        // 添加用户消息
        this.addMessage('user', message);
        
        // 显示加载状态
        const loadingId = this.addLoadingMessage();
        
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            const data = await response.json();
            
            // 移除加载消息
            this.removeLoadingMessage(loadingId);
            
            if (data.success) {
                this.addMessage('assistant', data.ai_message.content);
                this.messageCount += 2;
                this.updateMessageCount();
            } else {
                this.addMessage('assistant', '抱歉，发生了错误: ' + data.error);
            }
        } catch (error) {
            this.removeLoadingMessage(loadingId);
            this.addMessage('assistant', '网络错误，请稍后重试');
            console.error('发送消息失败:', error);
        }
        
        this.isLoading = false;
        this.updateSendButton(false);
        input.focus();
    }

    addMessage(role, content) {
        const container = document.getElementById('messagesContainer');
        const welcomeMsg = document.getElementById('welcomeMessage');
        
        if (welcomeMsg) {
            welcomeMsg.style.display = 'none';
        }
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = role === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        // 处理换行和格式化
        const formattedContent = this.formatMessage(content);
        contentDiv.innerHTML = formattedContent;
        
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = new Date().toLocaleTimeString();
        contentDiv.appendChild(timeDiv);
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(contentDiv);
        
        container.appendChild(messageDiv);
        container.scrollTop = container.scrollHeight;
    }

    formatMessage(content) {
        // 简单的文本格式化
        return content
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code>$1</code>');
    }

    addLoadingMessage() {
        const container = document.getElementById('messagesContainer');
        const loadingId = 'loading-' + Date.now();
        
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message assistant';
        messageDiv.id = loadingId;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = '<i class="fas fa-robot"></i>';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.innerHTML = `
            <div class="loading">
                <span>AI正在思考</span>
                <div class="loading-dots">
                    <div class="loading-dot"></div>
                    <div class="loading-dot"></div>
                    <div class="loading-dot"></div>
                </div>
            </div>
        `;
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(contentDiv);
        
        container.appendChild(messageDiv);
        container.scrollTop = container.scrollHeight;
        
        return loadingId;
    }

    removeLoadingMessage(loadingId) {
        const loadingMsg = document.getElementById(loadingId);
        if (loadingMsg) {
            loadingMsg.remove();
        }
    }

    updateSendButton(loading) {
        const btn = document.getElementById('sendBtn');
        btn.disabled = loading;
        btn.innerHTML = loading ? '<i class="fas fa-spinner fa-spin"></i>' : '<i class="fas fa-paper-plane"></i>';
    }

    async clearChat() {
        try {
            await fetch('/api/clear', { method: 'POST' });
            const container = document.getElementById('messagesContainer');
            const modelName = document.getElementById('modelBadge').textContent.replace('🧠 ', '');
            
            container.innerHTML = `
                <div class="welcome-message" id="welcomeMessage">
                    <h2>🚀 欢迎使用 Unlimited Agent</h2>
                    <p>这是一个基于 ${modelName} 的AI助手</p>
                    <p>开始对话，体验无限制的AI交流！</p>
                </div>
            `;
            this.messageCount = 0;
            this.updateMessageCount();
        } catch (error) {
            console.error('清空聊天失败:', error);
        }
    }

    async loadChatHistory() {
        try {
            const response = await fetch('/api/history');
            const data = await response.json();
            
            if (data.messages && data.messages.length > 0) {
                document.getElementById('welcomeMessage').style.display = 'none';
                
                data.messages.forEach(msg => {
                    this.addMessage(msg.role, msg.content);
                });
                
                this.messageCount = data.messages.length;
                this.updateMessageCount();
            }
        } catch (error) {
            console.error('加载历史失败:', error);
        }
    }

    async checkStatus() {
        try {
            const response = await fetch('/api/config');
            const data = await response.json();
            
            const statusDot = document.getElementById('statusDot');
            const statusText = document.getElementById('statusText');
            
            if (data.has_model) {
                statusDot.classList.remove('offline');
                statusText.textContent = '模型已就绪';
            } else {
                statusDot.classList.add('offline');
                statusText.textContent = '演示模式';
            }
        } catch (error) {
            const statusDot = document.getElementById('statusDot');
            const statusText = document.getElementById('statusText');
            statusDot.classList.add('offline');
            statusText.textContent = '连接失败';
            console.error('状态检查失败:', error);
        }
    }

    updateMessageCount() {
        document.getElementById('messageCount').textContent = `消息: ${this.messageCount}`;
    }

    toggleTheme() {
        const body = document.body;
        
        if (this.currentTheme === 'dark') {
            body.setAttribute('data-theme', 'light');
            this.currentTheme = 'light';
        } else {
            body.setAttribute('data-theme', 'dark');
            this.currentTheme = 'dark';
        }
        
        this.updateThemeIcon();
    }

    updateThemeIcon() {
        const themeIcon = document.getElementById('themeIcon');
        if (this.currentTheme === 'dark') {
            themeIcon.className = 'fas fa-sun';
        } else {
            themeIcon.className = 'fas fa-moon';
        }
    }
}

// 全局函数（用于HTML中的onclick事件）
let chatApp;

function sendMessage() {
    if (chatApp) chatApp.sendMessage();
}

function clearChat() {
    if (chatApp) chatApp.clearChat();
}

function toggleTheme() {
    if (chatApp) chatApp.toggleTheme();
}

// 初始化应用
document.addEventListener('DOMContentLoaded', function() {
    chatApp = new ChatApp();
});