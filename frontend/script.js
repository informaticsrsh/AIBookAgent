document.addEventListener('DOMContentLoaded', () => {
    // Chat elements
    const chatMessages = document.getElementById('chat-messages');
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-button');

    // Settings modal elements
    const settingsModal = document.getElementById('settings-modal');
    const settingsButton = document.getElementById('settings-button');
    const closeButton = document.querySelector('.close-button');
    const saveApiKeyButton = document.getElementById('save-api-key-button');
    const apiKeyInput = document.getElementById('api-key-input');

    // --- Settings Modal Logic ---
    settingsButton.onclick = () => {
        settingsModal.style.display = 'block';
    };

    closeButton.onclick = () => {
        settingsModal.style.display = 'none';
    };

    window.onclick = (event) => {
        if (event.target == settingsModal) {
            settingsModal.style.display = 'none';
        }
    };

    saveApiKeyButton.onclick = () => {
        const apiKey = apiKeyInput.value.trim();
        if (apiKey) {
            localStorage.setItem('gemini-api-key', apiKey);
            settingsModal.style.display = 'none';
            alert('API Key saved!');
        } else {
            alert('Please enter a valid API Key.');
        }
    };

    // --- Chat Logic ---
    const addMessage = (text, sender) => {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);
        messageElement.textContent = text;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    const handleSendMessage = async () => {
        const text = chatInput.value.trim();
        const apiKey = localStorage.getItem('gemini-api-key');

        if (!apiKey) {
            addMessage('Please set your Gemini API Key in the settings.', 'bot');
            return;
        }

        if (text) {
            addMessage(text, 'user');
            chatInput.value = '';

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ text, api_key: apiKey }),
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.detail || 'Something went wrong');
                }

                const data = await response.json();
                addMessage(data.response, 'bot');

            } catch (error) {
                console.error('Error:', error);
                addMessage(`Sorry, an error occurred: ${error.message}`, 'bot');
            }
        }
    };

    sendButton.addEventListener('click', handleSendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleSendMessage();
        }
    });
});
