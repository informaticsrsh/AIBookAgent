const API_BASE_URL = 'http://127.0.0.1:8000';

document.addEventListener('DOMContentLoaded', () => {
    // Existing elements
    const saveApiKeyBtn = document.getElementById('save-api-key-btn');
    const apiKeyInput = document.getElementById('api-key-input');
    const openBtn = document.getElementById('open-btn');
    const rulesFileInput = document.getElementById('rules-file');

    // New elements for core features
    const startBtn = document.getElementById('start-btn');
    const expandBtn = document.getElementById('expand-btn');
    const stopBtn = document.getElementById('stop-btn');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');

    let manuscript = ''; // Variable to hold the clean manuscript
    let abortController = null; // To handle request cancellation

    // Function to load the initial manuscript
    function loadInitialManuscript() {
        fetch(`${API_BASE_URL}/get_book`)
            .then(response => response.text())
            .then(initialManuscript => {
                manuscript = initialManuscript;
                if (manuscript) {
                    addMessage('System', 'Loaded existing manuscript.');
                }
            })
            .catch(error => console.error('Error fetching manuscript:', error));
    }

    // Helper function to add messages to the chat window
    function addMessage(sender, text, isThinking = false) {
        const messageElement = document.createElement('div');
        if (isThinking) {
            messageElement.id = 'thinking-message';
        }
        messageElement.classList.add('message', `${sender.toLowerCase()}-message`);
        messageElement.innerHTML = `<strong>${sender}:</strong> ${text}`;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll to bottom
    }

    saveApiKeyBtn.addEventListener('click', () => {
        const apiKey = apiKeyInput.value;
        if (apiKey) {
            localStorage.setItem('apiKey', apiKey);
            alert('API key saved locally.');
            apiKeyInput.value = '';
        } else {
            alert('Please enter an API key');
        }
    });

    openBtn.addEventListener('click', () => {
        window.open(`${API_BASE_URL}/get_book`, '_blank');
    });

    rulesFileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const formData = new FormData();
            formData.append('file', file);
            fetch(`${API_BASE_URL}/save_rules`, {
                method: 'POST',
                body: formData,
            })
            .then(response => response.json())
            .then(data => alert(data.message))
            .catch(error => console.error('Error:', error));
        }
    });

    startBtn.addEventListener('click', () => {
        const prompt = chatInput.value;
        const apiKey = localStorage.getItem('apiKey');
        if (!apiKey) {
            alert('Please save your API key first.');
            return;
        }
        if (prompt) {
            abortController = new AbortController();
            addMessage('User', prompt);
            chatInput.value = '';
            addMessage('Agent', 'Thinking...', true);

            fetch(`${API_BASE_URL}/generate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${apiKey}`
                },
                body: JSON.stringify({ prompt: prompt }),
                signal: abortController.signal
            })
            .then(response => {
                document.getElementById('thinking-message')?.remove();
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                addMessage('Agent', data.message);
                manuscript += '\n\n' + data.message; // Append to manuscript
            })
            .catch(error => {
                document.getElementById('thinking-message')?.remove();
                if (error.name === 'AbortError') {
                    addMessage('System', 'Request cancelled.');
                } else {
                    addMessage('System', `Error: ${error.message}`);
                }
            });
        }
    });

    expandBtn.addEventListener('click', () => {
        const apiKey = localStorage.getItem('apiKey');
        if (!apiKey) {
            alert('Please save your API key first.');
            return;
        }
        abortController = new AbortController();
        addMessage('System', 'Expand command sent.');
        addMessage('Agent', 'Thinking...', true);
        fetch(`${API_BASE_URL}/expand`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${apiKey}`
            },
            signal: abortController.signal,
        })
        .then(response => {
            document.getElementById('thinking-message')?.remove();
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            addMessage('Agent', data.message);
            manuscript += '\n\n' + data.message; // Append the new passage
        })
        .catch(error => {
            document.getElementById('thinking-message')?.remove();
            if (error.name === 'AbortError') {
                addMessage('System', 'Request cancelled.');
            } else {
                addMessage('System', `Error: ${error.message}`);
            }
        });
    });

    stopBtn.addEventListener('click', () => {
        if (abortController) {
            abortController.abort();
            abortController = null;
        }
    });

    // Load the manuscript when the page loads
    loadInitialManuscript();
});
