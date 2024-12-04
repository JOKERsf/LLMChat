document.addEventListener('DOMContentLoaded', function() {
    const messageContainer = document.getElementById('messageContainer');
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');

    const botAvatar = `
        <svg class="w-8 h-8" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="10" fill="#8B5CF6"/>
            <path d="M12 14.5C10.067 14.5 8.5 12.933 8.5 11C8.5 9.067 10.067 7.5 12 7.5C13.933 7.5 15.5 9.067 15.5 11C15.5 12.933 13.933 14.5 12 14.5Z" fill="white"/>
            <path d="M12 16.5C9.0975 16.5 6.75 15.15 6.75 13.5C6.75 11.85 9.0975 10.5 12 10.5C14.9025 10.5 17.25 11.85 17.25 13.5C17.25 15.15 14.9025 16.5 12 16.5Z" fill="white"/>
        </svg>
    `;

    const userAvatar = `
        <svg class="w-8 h-8" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="10" fill="#3B82F6"/>
            <path d="M12 13C13.6569 13 15 11.6569 15 10C15 8.34315 13.6569 7 12 7C10.3431 7 9 8.34315 9 10C9 11.6569 10.3431 13 12 13Z" fill="white"/>
            <path d="M18 18C18 15.2386 15.3137 13 12 13C8.68629 13 6 15.2386 6 18" stroke="white" stroke-width="2"/>
        </svg>
    `;

    function addMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'flex gap-3';
        messageElement.innerHTML = `
            <div class="flex-shrink-0">
                ${message.isBot ? botAvatar : userAvatar}
            </div>
            <div class="flex-1">
                <div class="bg-white p-4 rounded shadow">
                    <p class="whitespace-pre-wrap">${message.content}</p>
                </div>
                <div class="flex items-center gap-2 mt-2">
                    <span class="text-sm text-gray-500">${message.timestamp}</span>
                    <div class="flex gap-1 ml-auto">
                        <button class="text-gray-500 hover:text-gray-700">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                            </svg>
                        </button>
                        <button class="text-gray-500 hover:text-gray-700">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                            </svg>
                        </button>
                        <button class="text-gray-500 hover:text-gray-700">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
                            </svg>
                        </button>
                        <button class="text-gray-500 hover:text-gray-700">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14H5.236a2 2 0 01-1.789-2.894l3.5-7A2 2 0 018.736 3h4.018a2 2 0 01.485.06l3.76.94m-7 10v5a2 2 0 002 2h.096c.5 0 .905-.405.905-.904 0-.715.211-1.413.608-2.008L17 13V4m-7 10h2m5-10h2a2 2 0 012 2v6a2 2 0 01-2 2h-2.5" />
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        `;
        messageContainer.appendChild(messageElement);
        messageContainer.scrollTop = messageContainer.scrollHeight;
    }

    async function sendMessage() {
        const content = messageInput.value.trim();
        if (content) {
            // 添加用户消息到界面
            addMessage({
                content: content,
                isBot: false,
                timestamp: new Date().toLocaleString('zh-CN')
            });

            // 清空输入框
            messageInput.value = '';

            try {
                // 调用后端API
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: content }),
                });

                if (!response.ok) {
                    throw new Error('API请求失败');
                }

                const data = await response.json();

                // 添加机器人回复到界面
                addMessage({
                    content: data.reply,
                    isBot: true,
                    timestamp: new Date().toLocaleString('zh-CN')
                });
            } catch (error) {
                console.error('发送消息时出错:', error);
                // 可以在这里添加错误处理，比如显示一条错误消息
                addMessage({
                    content: "抱歉，发生了一个错误。请稍后再试。",
                    isBot: true,
                    timestamp: new Date().toLocaleString('zh-CN')
                });
            }
        }
    }

    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.ctrlKey) {
            e.preventDefault();
            sendMessage();
        }
    });
});

