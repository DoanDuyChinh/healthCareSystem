import random
from datetime import datetime

# Sample responses for different types of healthcare queries
GREETINGS = [
    "Hello! How can I assist you with your healthcare needs today?",
    "Hi there! Welcome to our healthcare chatbot. How may I help you?",
    "Greetings! I'm here to help with your healthcare questions.",
]

MEDICAL_SYMPTOMS = {
    "headache": "Headaches can be caused by various factors including stress, dehydration, or eyestrain. If it's severe or persistent, please consult a doctor.",
    "fever": "Fever is often a sign that your body is fighting an infection. Rest, stay hydrated, and take over-the-counter fever reducers. Consult a doctor if it persists or is high.",
    "cough": "Coughs can be due to allergies, infections, or irritants. Stay hydrated and consider over-the-counter cough medicine. See a doctor if it's persistent or you have trouble breathing.",
    "pain": "Pain can have many causes. Try rest and over-the-counter pain relievers. If it's severe or persistent, please consult with a doctor.",
    "fatigue": "Fatigue can be caused by poor sleep, stress, or underlying health conditions. Ensure you're getting enough rest and proper nutrition.",
    "cold": "For cold symptoms, rest, stay hydrated, and consider over-the-counter medications for symptom relief. See a doctor if symptoms worsen or persist.",
    "flu": "Flu symptoms include fever, body aches, and fatigue. Rest, stay hydrated, and take over-the-counter medications for symptoms. See a doctor for severe symptoms.",
}

APPOINTMENT_RESPONSES = [
    "You can book an appointment through the 'Book Appointment' section in your patient dashboard.",
    "To schedule an appointment, please use the appointment booking feature in your account.",
    "Appointments can be booked online through your patient portal or by calling our office.",
]

GENERAL_RESPONSES = [
    "I'm here to provide general healthcare information, but for specific medical advice, please consult with a healthcare professional.",
    "While I can offer general information, it's important to consult with a doctor for personalized medical advice.",
    "I can help with general healthcare questions, but remember to follow your doctor's advice for your specific healthcare needs.",
]

def generate_bot_response(message, user):
    """Generate a response based on the user's message."""
    message_lower = message.lower()
    
    # Check for greetings
    if any(greeting in message_lower for greeting in ["hello", "hi", "hey", "greetings"]):
        return random.choice(GREETINGS)
    
    # Check for appointment-related queries
    if any(term in message_lower for term in ["appointment", "schedule", "book", "visit", "doctor"]):
        return random.choice(APPOINTMENT_RESPONSES)
    
    # Check for symptom-related queries
    for symptom, response in MEDICAL_SYMPTOMS.items():
        if symptom in message_lower:
            return response
    
    # Check for medication or prescription queries
    if any(term in message_lower for term in ["medicine", "medication", "prescription", "drug", "pharmacy"]):
        return "For medication or prescription inquiries, please check the Pharmacy section in your dashboard or consult with your doctor."
    
    # Check for test-related queries
    if any(term in message_lower for term in ["test", "lab", "blood", "urine", "sample"]):
        return "For lab test information, please check the Lab Tests section in your dashboard or consult with your doctor."
    
    # Check for billing or payment queries
    if any(term in message_lower for term in ["bill", "payment", "insurance", "cost", "pay"]):
        return "For billing inquiries, please visit the Billing & Payment section in your dashboard or contact our billing department."
    
    # Check for profile-related queries
    if any(term in message_lower for term in ["profile", "account", "information", "details", "password"]):
        return "You can update your profile information in the Edit Profile section of your dashboard."
    
    # Default responses
    return random.choice(GENERAL_RESPONSES)
