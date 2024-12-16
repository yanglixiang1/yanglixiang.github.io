document.addEventListener('DOMContentLoaded', function() {
    const messagesDiv = document.getElementById('messages');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');

    // 添加消息到聊天框
    function addMessage(message, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = isUser ? 'user-message' : 'ai-message';
        messageDiv.style.margin = '10px';
        messageDiv.style.padding = '10px';
        messageDiv.style.borderRadius = '10px';
        messageDiv.style.maxWidth = '70%';
        messageDiv.style.alignSelf = isUser ? 'flex-end' : 'flex-start';
        messageDiv.style.background = isUser ? '#4CAF50' : '#2196F3';
        messageDiv.style.color = 'white';
        messageDiv.textContent = message;
        messagesDiv.appendChild(messageDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    // 发送消息到服务器
    async function sendMessage(message) {
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            const data = await response.json();
            return data.response;
        } catch (error) {
            console.error('Error:', error);
            return '抱歉，服务器出现错误。';
        }
    }

    // 处理发送按钮点击事件
    sendButton.addEventListener('click', async () => {
        const message = userInput.value.trim();
        if (message) {
            addMessage(message, true);
            userInput.value = '';
            const response = await sendMessage(message);
            addMessage(response);
        }
    });

    // 处理回车键发送消息
    userInput.addEventListener('keypress', async (e) => {
        if (e.key === 'Enter') {
            sendButton.click();
        }
    });
}); 