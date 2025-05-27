document.addEventListener('DOMContentLoaded', function() {
    console.log('Chat.js loaded successfully');
    
    const messageForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const chatMessages = document.querySelector('.chat-messages');
    const newConversationBtn = document.getElementById('new-conversation-btn');
    const conversationItems = document.querySelectorAll('.conversation-item');
    const deleteButtons = document.querySelectorAll('.delete-conversation-btn');
    
    // Get the conversation ID from the chat container
    function getConversationId() {
        const chatContainer = document.querySelector('.chat-container');
        return chatContainer ? chatContainer.dataset.conversationId : '';
    }
    
    // Get CSRF token
    function getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
    
    // Scroll to bottom of chat
    function scrollToBottom() {
        if (chatMessages) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }
    
    // Initial scroll to bottom
    scrollToBottom();
    
    // Add a temporary "typing" message
    function addTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message typing-indicator-container';
        typingDiv.innerHTML = `
            <div class="message-content">
                <div class="typing-indicator">
                    <span></span><span></span><span></span>
                </div>
            </div>
        `;
        chatMessages.appendChild(typingDiv);
        scrollToBottom();
        return typingDiv;
    }
    
    // Remove typing indicator
    function removeTypingIndicator() {
        const typingIndicator = document.querySelector('.typing-indicator-container');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    // Handle message submission
    if (messageForm) {
        messageForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const message = messageInput.value.trim();
            if (!message) return;
            
            // Add user message to UI
            const userMessageDiv = document.createElement('div');
            userMessageDiv.className = 'message user-message';
            userMessageDiv.innerHTML = `
                <div class="message-content">${message.replace(/\n/g, '<br>')}</div>
                <div class="message-time">${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div>
            `;
            chatMessages.appendChild(userMessageDiv);
            
            // Clear input
            messageInput.value = '';
            
            // Scroll to bottom
            scrollToBottom();
            
            // Show typing indicator
            const typingIndicator = addTypingIndicator();
            
            // Send message to server
            fetch('/chatbot/send_message/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({
                    message: message,
                    conversation_id: getConversationId()
                })
            })
            .then(response => response.json())
            .then(data => {
                // Remove typing indicator
                removeTypingIndicator();
                
                if (data.status === 'success') {
                    // If it's a new conversation, reload the page to update sidebar
                    if (!getConversationId()) {
                        window.location.href = `/chatbot/chat/?conversation_id=${data.conversation_id}`;
                        return;
                    }
                    
                    // Add bot response to UI
                    if (data.bot_message) {
                        const botMessageDiv = document.createElement('div');
                        botMessageDiv.className = 'message bot-message';
                        botMessageDiv.innerHTML = `
                            <div class="message-content">${data.bot_message.content.replace(/\n/g, '<br>')}</div>
                            <div class="message-time">${data.bot_message.timestamp}</div>
                        `;
                        chatMessages.appendChild(botMessageDiv);
                        
                        // Scroll to bottom
                        scrollToBottom();
                    }
                } else {
                    console.error('Error:', data.message);
                    
                    // Show error message
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'message bot-message';
                    errorDiv.innerHTML = `
                        <div class="message-content text-danger">Sorry, an error occurred. Please try again.</div>
                        <div class="message-time">${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div>
                    `;
                    chatMessages.appendChild(errorDiv);
                    scrollToBottom();
                }
            })
            .catch(error => {
                console.error('Error:', error);
                removeTypingIndicator();
                
                // Show error message
                const errorDiv = document.createElement('div');
                errorDiv.className = 'message bot-message';
                errorDiv.innerHTML = `
                    <div class="message-content text-danger">Network error. Please check your connection and try again.</div>
                    <div class="message-time">${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div>
                `;
                chatMessages.appendChild(errorDiv);
                scrollToBottom();
            });
        });
    }
    
    // Create new conversation
    if (newConversationBtn) {
        newConversationBtn.addEventListener('click', function() {
            fetch('/chatbot/create_conversation/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken()
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    window.location.href = `/chatbot/chat/?conversation_id=${data.conversation_id}`;
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }
    
    // Navigate to conversation
    conversationItems.forEach(item => {
        item.addEventListener('click', function(e) {
            // Don't navigate if clicking the delete button
            if (e.target.closest('.delete-conversation-btn')) return;
            
            const id = this.dataset.conversationId;
            window.location.href = `/chatbot/chat/?conversation_id=${id}`;
        });
    });
    
    // Delete conversation
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation();
            
            if (confirm('Are you sure you want to delete this conversation?')) {
                const id = this.dataset.conversationId;
                
                fetch(`/chatbot/delete_conversation/${id}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCsrfToken()
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        window.location.href = '/chatbot/chat/';
                    }
                })
                .catch(error => console.error('Error:', error));
            }
        });
    });
});
