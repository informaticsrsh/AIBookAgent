document.addEventListener('DOMContentLoaded', () => {
    // Chat elements
    const chatMessages = document.getElementById('chat-messages');
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-button');
    const stopButton = document.getElementById('stop-button');

    // Settings modal elements
    const settingsModal = document.getElementById('settings-modal');
    const settingsButton = document.getElementById('settings-button');
    const closeButton = document.querySelector('.close-button');
    const saveSettingsButton = document.getElementById('save-settings-button');
    const apiKeyInput = document.getElementById('api-key-input');
    const flashRpmInput = document.getElementById('flash-rpm-input');
    const proRpmInput = document.getElementById('pro-rpm-input');
    const agentARoleInput = document.getElementById('agent-a-role-input');
    const agentBRoleInput = document.getElementById('agent-b-role-input');

    let isDebateActive = false;
    let historyPollingInterval;

    // --- Settings Modal Logic ---
    settingsButton.onclick = () => {
        settingsModal.style.display = 'block';
        loadSettings();
    };

    closeButton.onclick = () => {
        settingsModal.style.display = 'none';
    };

    window.onclick = (event) => {
        if (event.target == settingsModal) {
            settingsModal.style.display = 'none';
        }
    };

    saveSettingsButton.onclick = () => {
        localStorage.setItem('gemini-api-key', apiKeyInput.value.trim());
        localStorage.setItem('flash-rpm', flashRpmInput.value);
        localStorage.setItem('pro-rpm', proRpmInput.value);
        localStorage.setItem('agent-a-role', agentARoleInput.value);
        localStorage.setItem('agent-b-role', agentBRoleInput.value);
        settingsModal.style.display = 'none';
        alert('Settings saved!');
    };

    const loadSettings = () => {
        apiKeyInput.value = localStorage.getItem('gemini-api-key') || '';
        flashRpmInput.value = localStorage.getItem('flash-rpm') || '15';
        proRpmInput.value = localStorage.getItem('pro-rpm') || '2';
        agentARoleInput.value = localStorage.getItem('agent-a-role') || 'You are a helpful assistant.';
        agentBRoleInput.value = localStorage.getItem('agent-b-role') || 'You are a critical thinker.';
    };

    // --- Chat Logic ---
    const addMessage = (text, sender) => {
        const messageElement = document.createElement('div');
        let senderClass = '';
        switch (sender) {
            case 'User':
                senderClass = 'user-message';
                break;
            case 'Agent A':
                senderClass = 'agent-a-message';
                break;
            case 'Agent B':
                senderClass = 'agent-b-message';
                break;
            default:
                senderClass = 'bot-message';
        }
        messageElement.classList.add('message', senderClass);
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
            chatMessages.innerHTML = ''; // Clear chat on new topic
            addMessage(text, 'User');
            chatInput.value = '';

            const debateSettings = {
                topic: text,
                api_key: apiKey,
                agent_a_role: localStorage.getItem('agent-a-role'),
                agent_b_role: localStorage.getItem('agent-b-role'),
                flash_rpm: parseInt(flashRpmInput.value),
                pro_rpm: parseInt(proRpmInput.value),
            };

            try {
                const response = await fetch('/api/debate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(debateSettings),
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.detail || 'Failed to start debate');
                }

                setDebateState(true);

            } catch (error) {
                console.error('Error:', error);
                addMessage(`Error starting debate: ${error.message}`, 'bot');
            }
        }
    };

    const setDebateState = (isActive) => {
        isDebateActive = isActive;
        stopButton.style.display = isActive ? 'block' : 'none';
        sendButton.style.display = isActive ? 'none' : 'block';
        if(isActive) {
            historyPollingInterval = setInterval(fetchHistory, 2000);
        } else {
            clearInterval(historyPollingInterval);
        }
    };

    const fetchHistory = async () => {
        try {
            const response = await fetch('/api/history');
            const data = await response.json();
            chatMessages.innerHTML = '';
            data.history.forEach(msg => addMessage(msg.text, msg.sender));
        } catch (error) {
            console.error('Error fetching history:', error);
        }
    };

    stopButton.addEventListener('click', async () => {
        try {
            await fetch('/api/stop', { method: 'POST' });
            setDebateState(false);
        } catch (error) {
            console.error('Error stopping debate:', error);
        }
    });

    sendButton.addEventListener('click', handleSendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleSendMessage();
        }
    });

    loadSettings();
});
