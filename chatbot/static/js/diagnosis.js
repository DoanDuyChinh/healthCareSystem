// AI Diagnosis functionality
class AIDiagnosis {
    constructor() {
        this.currentLanguage = 'en'; // Default to English
        this.symptoms = {
            'en': [], // Will be populated from the server
            'vi': []  // Will be populated from the server
        };
        this.selectedSymptoms = [];
        this.symptomVectors = {
            'en': {},
            'vi': {}
        };
        this.conversationId = null;
        
        // Initialize event listeners
        this.initEventListeners();
        
        console.log("AIDiagnosis initialized");
    }
    
    initEventListeners() {
        // Listen for AI diagnosis button click
        document.addEventListener('click', (e) => {
            if (e.target && (e.target.id === 'ai-diagnosis-btn' || e.target.closest('#ai-diagnosis-btn'))) {
                console.log("AI diagnosis button clicked");
                this.showDiagnosisModal();
            }
        });
        
        // Close modal when clicking outside or on close button
        document.addEventListener('click', (e) => {
            if (e.target && e.target.id === 'diagnosis-modal-backdrop') {
                this.hideDiagnosisModal();
            }
            if (e.target && e.target.id === 'close-diagnosis-modal') {
                this.hideDiagnosisModal();
            }
        });
        
        // Listen for start diagnosis button click
        document.addEventListener('click', (e) => {
            if (e.target && e.target.id === 'start-diagnosis-btn') {
                this.startDiagnosis();
            }
        });
    }
    
    // Load symptoms from the server
    loadSymptoms(enSymptoms, viSymptoms) {
        this.symptoms.en = enSymptoms;
        this.symptoms.vi = viSymptoms;
        
        // Create symptom vectors mapping
        enSymptoms.forEach((symptom, index) => {
            this.symptomVectors.en[symptom] = index;
        });
        
        viSymptoms.forEach((symptom, index) => {
            this.symptomVectors.vi[symptom] = index;
        });
        
        console.log("Symptoms loaded:", this.symptoms);
    }
    
    // Set the current conversation ID
    setConversationId(id) {
        this.conversationId = id;
    }
    
    // Set the current language
    setLanguage(lang) {
        this.currentLanguage = lang;
        this.updateButtonText();
    }
    
    // Update the button text based on language
    updateButtonText() {
        const btnText = document.querySelector('.diagnosis-btn-text');
        if (btnText) {
            btnText.textContent = this.currentLanguage === 'vi' ? 'Chẩn Đoán AI' : 'AI Diagnosis';
        }
    }
    
    // Show the diagnosis modal
    showDiagnosisModal() {
        // First, detect current language from recent messages
        this.detectCurrentLanguage();
        
        // Create and show the modal
        const symptomsHtml = this.createSymptomsCheckboxes();
        const modalTitle = this.currentLanguage === 'vi' ? 'Chẩn Đoán AI' : 'AI Diagnosis';
        const startBtnText = this.currentLanguage === 'vi' ? 'Bắt Đầu Chẩn Đoán' : 'Start Diagnosis';
        const instructions = this.currentLanguage === 'vi' 
            ? 'Vui lòng chọn các triệu chứng bạn đang gặp phải:' 
            : 'Please select the symptoms you are experiencing:';
        
        const modalHtml = `
        <div id="diagnosis-modal-backdrop" class="diagnosis-modal-backdrop">
            <div class="diagnosis-modal">
                <div class="diagnosis-modal-header">
                    <h3>${modalTitle}</h3>
                    <button id="close-diagnosis-modal" class="close-btn">&times;</button>
                </div>
                <div class="diagnosis-modal-body">
                    <p>${instructions}</p>
                    <div class="symptoms-container">
                        ${symptomsHtml}
                    </div>
                </div>
                <div class="diagnosis-modal-footer">
                    <button id="start-diagnosis-btn" class="primary-btn">${startBtnText}</button>
                </div>
            </div>
        </div>
        `;
        
        // Add modal to the DOM
        const modalContainer = document.createElement('div');
        modalContainer.innerHTML = modalHtml;
        document.body.appendChild(modalContainer);
        
        // Add event listeners to checkboxes
        document.querySelectorAll('.symptom-checkbox').forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                const symptomName = e.target.value;
                if (e.target.checked) {
                    this.selectedSymptoms.push(symptomName);
                } else {
                    const index = this.selectedSymptoms.indexOf(symptomName);
                    if (index !== -1) {
                        this.selectedSymptoms.splice(index, 1);
                    }
                }
            });
        });
    }
    
    // Hide the diagnosis modal
    hideDiagnosisModal() {
        const backdrop = document.getElementById('diagnosis-modal-backdrop');
        if (backdrop) {
            backdrop.remove();
        }
        this.selectedSymptoms = [];
    }
    
    // Create checkboxes for symptoms
    createSymptomsCheckboxes() {
        const symptoms = this.symptoms[this.currentLanguage];
        let html = '';
        
        symptoms.forEach(symptom => {
            html += `
            <div class="symptom-checkbox-container">
                <input type="checkbox" id="symptom-${this.sanitizeId(symptom)}" class="symptom-checkbox" value="${symptom}">
                <label for="symptom-${this.sanitizeId(symptom)}">${symptom}</label>
            </div>
            `;
        });
        
        return html;
    }
    
    // Sanitize string for use as an ID
    sanitizeId(str) {
        return str.toString().toLowerCase().replace(/[^a-z0-9]/g, '-');
    }
    
    // Detect current language from messages
    detectCurrentLanguage() {
        // Look for language indicators in the last few messages
        const messages = document.querySelectorAll('.message-content');
        if (messages.length > 0) {
            const lastMessages = Array.from(messages).slice(-3); // Get last 3 messages
            const combinedText = lastMessages.map(msg => msg.textContent).join(' ').toLowerCase();
            
            // Check for Vietnamese indicators
            const viIndicators = ['tôi', 'bạn', 'của', 'và', 'hoặc', 'không', 'có', 'đã', 'vui lòng', 'xin chào'];
            const hasViIndicators = viIndicators.some(word => combinedText.includes(word));
            
            this.currentLanguage = hasViIndicators ? 'vi' : 'en';
            this.updateButtonText();
        }
    }
    
    // Start the diagnosis process
    startDiagnosis() {
        if (this.selectedSymptoms.length === 0) {
            const message = this.currentLanguage === 'vi' 
                ? 'Vui lòng chọn ít nhất một triệu chứng.' 
                : 'Please select at least one symptom.';
            alert(message);
            return;
        }
        
        // Create symptom vector array (0 or 1 for each symptom)
        const symptomVector = Array(this.symptoms.en.length).fill(0);
        
        // Set 1 for selected symptoms
        this.selectedSymptoms.forEach(symptom => {
            const index = this.symptomVectors[this.currentLanguage][symptom];
            if (index !== undefined) {
                symptomVector[index] = 1;
            }
        });
        
        // Show loading in chat
        const loadingMessage = this.currentLanguage === 'vi' 
            ? 'Đang phân tích triệu chứng...' 
            : 'Analyzing symptoms...';
        this.addTemporaryMessage(loadingMessage);
        
        // Send to server
        this.sendDiagnosisRequest(symptomVector);
        
        // Close the modal
        this.hideDiagnosisModal();
    }
    
    // Add a temporary message to the chat
    addTemporaryMessage(message) {
        // Create a temporary message element
        const tempMessage = document.createElement('div');
        tempMessage.className = 'message bot-message temp-message';
        tempMessage.innerHTML = `
            <div class="message-content">${message}</div>
            <div class="message-time">${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div>
        `;
        
        // Add to chat container
        const chatContainer = document.querySelector('.chat-messages');
        if (chatContainer) {
            chatContainer.appendChild(tempMessage);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        return tempMessage;
    }
    
    // Send diagnosis request to server
    sendDiagnosisRequest(symptomVector) {
        fetch('/chatbot/ai_diagnosis/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCsrfToken()
            },
            body: JSON.stringify({
                conversation_id: this.conversationId,
                symptoms: symptomVector,
                language: this.currentLanguage
            })
        })
        .then(response => response.json())
        .then(data => {
            // Remove temporary message
            document.querySelectorAll('.temp-message').forEach(el => el.remove());
            
            if (data.status === 'success') {
                // Append the diagnosis message to the chat
                this.appendDiagnosisToChat(data.message_content, data.timestamp);
            } else {
                // Show error
                const errorMsg = this.currentLanguage === 'vi'
                    ? 'Đã xảy ra lỗi khi thực hiện chẩn đoán.'
                    : 'An error occurred while performing the diagnosis.';
                this.appendDiagnosisToChat(errorMsg, new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            // Remove temporary message
            document.querySelectorAll('.temp-message').forEach(el => el.remove());
            
            // Show error
            const errorMsg = this.currentLanguage === 'vi'
                ? 'Đã xảy ra lỗi khi kết nối với máy chủ.'
                : 'An error occurred while connecting to the server.';
            this.appendDiagnosisToChat(errorMsg, new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}));
        });
    }
    
    // Append diagnosis result to chat
    appendDiagnosisToChat(content, timestamp) {
        // Create a new message element
        const messageElement = document.createElement('div');
        messageElement.className = 'message bot-message';
        messageElement.innerHTML = `
            <div class="message-content">${content}</div>
            <div class="message-time">${timestamp}</div>
        `;
        
        // Add to chat container
        const chatContainer = document.querySelector('.chat-messages');
        if (chatContainer) {
            chatContainer.appendChild(messageElement);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    }
    
    // Get CSRF token
    getCsrfToken() {
        const tokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
        if (tokenElement) {
            return tokenElement.value;
        }
        // Fallback to getting from cookie
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith('csrftoken=')) {
                return cookie.substring('csrftoken='.length);
            }
        }
        return '';
    }
}

// Initialize diagnosis on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM loaded, initializing AI Diagnosis");
    
    // Get symptom lists from the page
    try {
        const symptomsEnEl = document.getElementById('symptoms-en-data');
        const symptomsViEl = document.getElementById('symptoms-vi-data');
        
        if (symptomsEnEl && symptomsViEl) {
            console.log("Found symptom data elements");
            const symptomsEn = JSON.parse(symptomsEnEl.textContent);
            const symptomsVi = JSON.parse(symptomsViEl.textContent);
            
            // Create global instance
            window.aiDiagnosis = new AIDiagnosis();
            
            // Load symptoms
            window.aiDiagnosis.loadSymptoms(symptomsEn, symptomsVi);
            
            // Set initial conversation ID
            const chatContainer = document.querySelector('.chat-container');
            if (chatContainer && chatContainer.dataset.conversationId) {
                window.aiDiagnosis.setConversationId(chatContainer.dataset.conversationId);
            }
        } else {
            console.error('Symptom data elements not found');
        }
    } catch (error) {
        console.error('Error loading symptom data:', error);
    }
    
    // Check if diagnosis button exists
    const diagnosisBtn = document.getElementById('ai-diagnosis-btn');
    if (diagnosisBtn) {
        console.log("AI Diagnosis button found in DOM");
    } else {
        console.error("AI Diagnosis button not found in DOM");
    }
});

// Add a direct way to check if everything is loaded properly
console.log("Diagnosis.js script loaded");
