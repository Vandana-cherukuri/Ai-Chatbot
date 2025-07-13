// Get DOM elements
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');

// Add event listeners
messageInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

sendButton.addEventListener('click', function() {
    sendMessage();
});

// Function to send message
async function sendMessage() {
    const message = messageInput.value.trim();
    
    if (!message) return;
    
    // Clear input and disable button
    messageInput.value = '';
    sendButton.disabled = true;
    sendButton.textContent = 'Sending...';
    
    // Add user message to chat
    addMessage(message, 'user');
    
    // Add typing indicator
    addTypingIndicator();
    
    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator();
        
        if (data.response) {
            // Add AI response to chat (already formatted as HTML)
            addMessage(data.response, 'bot');
        } else if (data.error) {
            // Handle error
            addMessage('Sorry, I encountered an error. Please try again.', 'error');
            console.error('Error:', data.error);
        }
    } catch (error) {
        // Remove typing indicator and show error
        removeTypingIndicator();
        addMessage('Sorry, I couldn\'t connect to the server. Please check your connection and try again.', 'error');
        console.error('Network error:', error);
    }
    
    // Re-enable button
    sendButton.disabled = false;
    sendButton.textContent = 'Send';
    
    // Focus back on input
    messageInput.focus();
}

// Function to add message to chat
function addMessage(content, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    if (sender === 'bot') {
        // For bot messages, content is already HTML from markdown processing
        messageDiv.innerHTML = content;
    } else {
        // For user messages, escape HTML and format normally
        messageDiv.textContent = content;
    }
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Function to add typing indicator
function addTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot typing-indicator';
    typingDiv.id = 'typingIndicator';
    
    typingDiv.innerHTML = `
        <div class="typing-indicator">
            <span>AI is typing</span>
            <div class="typing-dots">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
    `;
    
    chatMessages.appendChild(typingDiv);
    scrollToBottom();
}

// Function to remove typing indicator
function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Function to scroll to bottom of chat
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Initialize chat
document.addEventListener('DOMContentLoaded', function() {
    messageInput.focus();
});