const chatMessages = document.getElementById('chat-messages');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const statusDot = document.querySelector('.dot');
const statusText = document.getElementById('status');

// Determine the WebSocket URL based on the current page location
const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
const wsUrl = `${protocol}//${window.location.host}/ws/chat`;

let socket = new WebSocket(wsUrl);

// Handle connection open
socket.onopen = () => {
    console.log('WebSocket connection established');
    statusDot.style.backgroundColor = '#28a745';
    statusText.lastChild.textContent = ' Connected';
};

// Handle incoming messages
socket.onmessage = (event) => {
    addMessage(event.data, 'bot');
};

// Handle connection close
socket.onclose = () => {
    console.log('WebSocket connection closed');
    statusDot.style.backgroundColor = '#dc3545';
    statusText.lastChild.textContent = ' Disconnected';
    
    // Try to reconnect after a delay
    setTimeout(() => {
        statusText.lastChild.textContent = ' Reconnecting...';
        socket = new WebSocket(wsUrl);
    }, 3000);
};

// Handle form submission
chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const message = userInput.value.trim();
    
    if (message && socket.readyState === WebSocket.OPEN) {
        addMessage(message, 'user');
        socket.send(message);
        userInput.value = '';
    }
});

// Helper function to add a message bubble to the chat
function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
    messageDiv.textContent = text;
    
    chatMessages.appendChild(messageDiv);
    
    // Auto-scroll to the bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
