import random
from datetime import datetime
from doctors.models import DoctorProfile

# English responses
GREETINGS_EN = [
    "Hello! How can I assist you with your healthcare needs today?",
    "Hi there! Welcome to our healthcare chatbot. How may I help you?",
    "Greetings! I'm here to help with your healthcare questions.",
]

# Vietnamese responses
GREETINGS_VI = [
    "Xin chào! Tôi có thể hỗ trợ gì cho bạn về vấn đề sức khỏe hôm nay?",
    "Chào bạn! Chào mừng đến với trợ lý ảo y tế. Tôi có thể giúp gì cho bạn?",
    "Xin chào! Tôi ở đây để giúp đỡ bạn với các câu hỏi về sức khỏe.",
]

# English medical symptoms responses
MEDICAL_SYMPTOMS_EN = {
    "headache": "Headaches can be caused by various factors including stress, dehydration, or eyestrain. If it's severe or persistent, please consult a doctor.",
    "fever": "Fever is often a sign that your body is fighting an infection. Rest, stay hydrated, and take over-the-counter fever reducers. Consult a doctor if it persists or is high.",
    "cough": "Coughs can be due to allergies, infections, or irritants. Stay hydrated and consider over-the-counter cough medicine. See a doctor if it's persistent or you have trouble breathing.",
    "pain": "Pain can have many causes. Try rest and over-the-counter pain relievers. If it's severe or persistent, please consult with a doctor.",
    "fatigue": "Fatigue can be caused by poor sleep, stress, or underlying health conditions. Ensure you're getting enough rest and proper nutrition.",
    "cold": "For cold symptoms, rest, stay hydrated, and consider over-the-counter medications for symptom relief. See a doctor if symptoms worsen or persist.",
    "flu": "Flu symptoms include fever, body aches, and fatigue. Rest, stay hydrated, and take over-the-counter medications for symptoms. See a doctor for severe symptoms.",
}

# Vietnamese medical symptoms responses
MEDICAL_SYMPTOMS_VI = {
    "đau đầu": "Đau đầu có thể do nhiều nguyên nhân như căng thẳng, mất nước, hoặc mỏi mắt. Nếu đau đầu dữ dội hoặc kéo dài, vui lòng đi khám bác sĩ.",
    "sốt": "Sốt thường là dấu hiệu cho thấy cơ thể đang chống lại nhiễm trùng. Hãy nghỉ ngơi, uống nhiều nước và dùng thuốc hạ sốt không kê đơn. Hãy đi khám nếu sốt cao hoặc kéo dài.",
    "ho": "Ho có thể do dị ứng, nhiễm trùng hoặc kích ứng. Uống nhiều nước và cân nhắc dùng thuốc ho không kê đơn. Đi khám nếu ho kéo dài hoặc khó thở.",
    "đau": "Đau có thể có nhiều nguyên nhân. Hãy nghỉ ngơi và dùng thuốc giảm đau không kê đơn. Nếu đau dữ dội hoặc kéo dài, vui lòng đi khám bác sĩ.",
    "mệt mỏi": "Mệt mỏi có thể do ngủ không đủ, căng thẳng hoặc các vấn đề sức khỏe tiềm ẩn. Hãy đảm bảo ngủ đủ giấc và dinh dưỡng hợp lý.",
    "cảm lạnh": "Đối với các triệu chứng cảm lạnh, hãy nghỉ ngơi, uống nhiều nước và cân nhắc dùng thuốc không kê đơn để giảm triệu chứng. Đi khám nếu các triệu chứng trở nên tồi tệ hoặc kéo dài.",
    "cúm": "Triệu chứng cúm bao gồm sốt, đau nhức cơ thể và mệt mỏi. Nghỉ ngơi, uống nhiều nước và dùng thuốc không kê đơn cho các triệu chứng. Đi khám nếu có triệu chứng nặng.",
}

# English appointment responses
APPOINTMENT_RESPONSES_EN = [
    "You can book an appointment through the 'Book Appointment' section in your patient dashboard.",
    "To schedule an appointment, please use the appointment booking feature in your account.",
    "Appointments can be booked online through your patient portal or by calling our office.",
]

# Vietnamese appointment responses
APPOINTMENT_RESPONSES_VI = [
    "Bạn có thể đặt lịch hẹn thông qua mục 'Đặt lịch hẹn' trong trang điều khiển của bệnh nhân.",
    "Để lên lịch hẹn, vui lòng sử dụng tính năng đặt lịch hẹn trong tài khoản của bạn.",
    "Lịch hẹn có thể được đặt trực tuyến thông qua cổng thông tin bệnh nhân hoặc bằng cách gọi điện đến văn phòng của chúng tôi.",
]

# English general responses
GENERAL_RESPONSES_EN = [
    "I'm here to provide general healthcare information, but for specific medical advice, please consult with a healthcare professional.",
    "While I can offer general information, it's important to consult with a doctor for personalized medical advice.",
    "I can help with general healthcare questions, but remember to follow your doctor's advice for your specific healthcare needs.",
]

# Vietnamese general responses
GENERAL_RESPONSES_VI = [
    "Tôi ở đây để cung cấp thông tin y tế chung, nhưng để có lời khuyên y tế cụ thể, vui lòng tham khảo ý kiến của chuyên gia y tế.",
    "Mặc dù tôi có thể cung cấp thông tin chung, điều quan trọng là phải tham khảo ý kiến bác sĩ để được tư vấn y tế cá nhân hóa.",
    "Tôi có thể giúp bạn với các câu hỏi về chăm sóc sức khỏe chung, nhưng hãy nhớ tuân theo lời khuyên của bác sĩ cho nhu cầu chăm sóc sức khỏe cụ thể của bạn.",
]

# Mapping medical conditions to relevant specialties in Vietnamese
CONDITION_TO_SPECIALTY = {
    # Tim mạch (Cardiology)
    "heart": "Tim mạch",
    "cardiac": "Tim mạch",
    "chest pain": "Tim mạch",
    "blood pressure": "Tim mạch",
    "tim": "Tim mạch",
    "mạch": "Tim mạch",
    "tim mạch": "Tim mạch",
    "đau ngực": "Tim mạch",
    "huyết áp": "Tim mạch",
    
    # Da liễu (Dermatology)
    "skin": "Da liễu",
    "rash": "Da liễu",
    "acne": "Da liễu",
    "da": "Da liễu",
    "da liễu": "Da liễu",
    "mụn": "Da liễu",
    "phát ban": "Da liễu",
    
    # Nội tiết (Endocrinology)
    "diabetes": "Nội tiết",
    "thyroid": "Nội tiết",
    "hormone": "Nội tiết",
    "tiểu đường": "Nội tiết",
    "nội tiết": "Nội tiết",
    "tuyến giáp": "Nội tiết",
    "hormone": "Nội tiết",
    
    # Tiêu hóa (Gastroenterology)
    "stomach": "Tiêu hóa",
    "digestive": "Tiêu hóa",
    "liver": "Tiêu hóa",
    "intestine": "Tiêu hóa",
    "dạ dày": "Tiêu hóa",
    "tiêu hóa": "Tiêu hóa",
    "gan": "Tiêu hóa",
    "ruột": "Tiêu hóa",
    
    # Huyết học (Hematology)
    "blood": "Huyết học",
    "anemia": "Huyết học",
    "máu": "Huyết học",
    "huyết học": "Huyết học",
    "thiếu máu": "Huyết học",
    
    # Ung thư (Oncology)
    "cancer": "Ung thư",
    "tumor": "Ung thư",
    "ung thư": "Ung thư",
    "u bướu": "Ung thư",
    
    # Xương khớp (Orthopedics)
    "bone": "Xương khớp",
    "joint": "Xương khớp",
    "fracture": "Xương khớp",
    "knee": "Xương khớp",
    "back pain": "Xương khớp",
    "xương": "Xương khớp",
    "khớp": "Xương khớp",
    "xương khớp": "Xương khớp",
    "gãy xương": "Xương khớp",
    "đau lưng": "Xương khớp",
    "đau khớp": "Xương khớp",
    
    # Nhi khoa (Pediatrics)
    "child": "Nhi khoa",
    "baby": "Nhi khoa",
    "infant": "Nhi khoa",
    "trẻ em": "Nhi khoa",
    "nhi": "Nhi khoa",
    "nhi khoa": "Nhi khoa",
    "em bé": "Nhi khoa",
    "trẻ sơ sinh": "Nhi khoa",
    
    # Tâm thần (Psychiatry)
    "mental": "Tâm thần",
    "depression": "Tâm thần",
    "anxiety": "Tâm thần",
    "stress": "Tâm thần",
    "tâm thần": "Tâm thần",
    "trầm cảm": "Tâm thần",
    "lo âu": "Tâm thần",
    "căng thẳng": "Tâm thần",
    
    # Hô hấp (Pulmonology)
    "lung": "Hô hấp",
    "breathing": "Hô hấp",
    "respiratory": "Hô hấp",
    "cough": "Hô hấp",
    "phổi": "Hô hấp",
    "hô hấp": "Hô hấp",
    "khó thở": "Hô hấp",
    "ho": "Hô hấp",
    
    # Thận (Nephrology)
    "kidney": "Thận",
    "urine": "Thận",
    "thận": "Thận",
    "nước tiểu": "Thận",
    
    # Mắt (Ophthalmology)
    "eye": "Mắt",
    "vision": "Mắt",
    "mắt": "Mắt",
    "thị lực": "Mắt",
    "nhìn mờ": "Mắt",
    
    # Tai mũi họng (Otolaryngology)
    "ear": "Tai mũi họng",
    "nose": "Tai mũi họng",
    "throat": "Tai mũi họng",
    "hearing": "Tai mũi họng",
    "tai": "Tai mũi họng",
    "mũi": "Tai mũi họng",
    "họng": "Tai mũi họng",
    "tai mũi họng": "Tai mũi họng",
    "nghe kém": "Tai mũi họng",
    
    # Thần kinh (Neurology)
    "brain": "Thần kinh",
    "nerve": "Thần kinh",
    "headache": "Thần kinh",
    "migraine": "Thần kinh",
    "não": "Thần kinh",
    "thần kinh": "Thần kinh",
    "đau đầu": "Thần kinh",
    "đau nửa đầu": "Thần kinh",
    
    # Sản khoa (Obstetrics)
    "pregnancy": "Sản khoa",
    "mang thai": "Sản khoa",
    "sản khoa": "Sản khoa",
    "thai kỳ": "Sản khoa",
    
    # Phụ khoa (Gynecology)
    "gynecology": "Phụ khoa",
    "women": "Phụ khoa",
    "phụ khoa": "Phụ khoa",
    "phụ nữ": "Phụ khoa",
}

# Vietnamese indicator words to detect Vietnamese language
VIETNAMESE_INDICATORS = [
    "tôi", "bạn", "anh", "chị", "em", "của", "và", "hoặc", "nhưng", "vì", "tại", "trong", "ngoài",
    "làm", "đi", "đến", "về", "với", "cho", "cần", "muốn", "được", "bị", "có", "không", "vẫn",
    "đang", "sẽ", "đã", "rồi", "xin", "cảm", "thấy", "biết", "thích", "yêu", "ghét", "mong", "mến",
    "xin chào", "cám ơn", "vui lòng", "xin lỗi", "tạm biệt", "khỏe không", "giúp", "hỏi"
]

def detect_language(message):
    """Detect if the message is in Vietnamese or English"""
    message_lower = message.lower()
    
    # Count Vietnamese indicator words
    vi_word_count = sum(1 for word in VIETNAMESE_INDICATORS if word in message_lower)
    
    # If we find Vietnamese indicators, return Vietnamese
    if vi_word_count > 0:
        return 'vi'
    else:
        return 'en'

def get_doctors_by_specialty(specialty, language='vi'):
    """Find doctors based on specialty."""
    try:
        doctors = DoctorProfile.objects.filter(specialty__icontains=specialty).select_related('user')[:3]
        
        if doctors:
            doctor_list = []
            for doctor in doctors:
                # Build doctor information with experience years
                experience_text = f"{doctor.experience_years} năm kinh nghiệm" if language == 'vi' else f"{doctor.experience_years} years of experience"
                
                # Check if the doctor has a profile picture
                avatar_info = ""
                if hasattr(doctor.user, 'profile_picture') and doctor.user.profile_picture:
                    if language == 'vi':
                        avatar_info = "\n(Bác sĩ có hình đại diện trong hồ sơ)"
                    else:
                        avatar_info = "\n(Doctor has a profile picture available)"
                
                # Format doctor information differently based on language
                if language == 'vi':
                    doctor_info = f"👨‍⚕️ Bác sĩ {doctor.user.get_full_name()} - {doctor.specialty}\n   • {experience_text}\n   • Phí tư vấn: ${doctor.consulting_fee}{avatar_info}"
                else:
                    doctor_info = f"👨‍⚕️ Dr. {doctor.user.get_full_name()} - {doctor.specialty}\n   • {experience_text}\n   • Consulting fee: ${doctor.consulting_fee}{avatar_info}"
                
                doctor_list.append(doctor_info)
            
            doctor_text = "\n\n".join(doctor_list)
            
            # Response with enhanced doctor information
            if language == 'vi':
                return f"Dựa trên nhu cầu của bạn, tôi giới thiệu các chuyên gia {specialty} sau:\n\n{doctor_text}\n\nBạn có thể đặt lịch hẹn với họ thông qua hệ thống đặt lịch của chúng tôi."
            else:
                return f"Based on your needs, I recommend the following {specialty} specialists:\n\n{doctor_text}\n\nYou can book an appointment with them through our appointment system."
        else:
            if language == 'vi':
                return f"Tôi không tìm thấy chuyên gia {specialty} nào trong hệ thống hiện tại. Vui lòng liên hệ bộ phận hỗ trợ để được giúp đỡ thêm."
            else:
                return f"I couldn't find any {specialty} specialists in our system currently. Please contact our help desk for more assistance."
    except Exception as e:
        if language == 'vi':
            return "Tôi đang gặp sự cố khi truy cập cơ sở dữ liệu bác sĩ. Vui lòng thử lại sau hoặc liên hệ bộ phận hỗ trợ để được trợ giúp."
        else:
            return "I'm having trouble accessing our doctor database right now. Please try again later or contact our help desk for assistance."

def generate_bot_response(message, user):
    """Generate a response based on the user's message."""
    message_lower = message.lower()
    
    # Detect language (Vietnamese or English)
    language = detect_language(message_lower)
    
    # Get the appropriate response sets based on detected language
    GREETINGS = GREETINGS_VI if language == 'vi' else GREETINGS_EN
    MEDICAL_SYMPTOMS = MEDICAL_SYMPTOMS_VI if language == 'vi' else MEDICAL_SYMPTOMS_EN
    APPOINTMENT_RESPONSES = APPOINTMENT_RESPONSES_VI if language == 'vi' else APPOINTMENT_RESPONSES_EN
    GENERAL_RESPONSES = GENERAL_RESPONSES_VI if language == 'vi' else GENERAL_RESPONSES_EN
    
    # Check for doctor recommendation requests - both English and Vietnamese
    if any(term in message_lower for term in ["find doctor", "recommend doctor", "need doctor", "looking for doctor", "specialist", "specializes", 
                                             "tìm bác sĩ", "giới thiệu bác sĩ", "cần bác sĩ", "đang tìm bác sĩ", "chuyên khoa", "chuyên gia"]):
        # Track which specialty was found in the message
        found_specialty = None
        
        # Try to identify specialty from the message
        for condition, specialty in CONDITION_TO_SPECIALTY.items():
            if condition in message_lower:
                found_specialty = specialty
                break
        
        # If we found a specialty, return doctors for that specialty
        if found_specialty:
            return get_doctors_by_specialty(found_specialty, language)
        
        # No specific specialty mentioned
        if language == 'vi':
            return "Tôi có thể giúp bạn tìm bác sĩ. Vui lòng cho tôi biết bạn đang tìm kiếm bác sĩ về bệnh gì hoặc chuyên khoa nào? Ví dụ: 'Tôi cần bác sĩ tim mạch' hoặc 'Tôi đang tìm bác sĩ da liễu'."
        else:
            return "I can help you find a doctor. Could you please tell me what medical condition or specialty you're looking for? For example, 'I need a heart doctor' or 'I'm looking for a skin specialist'."
    
    # Check direct specialty mentions
    found_specialty = None
    
    # First check for exact specialty names in the message
    for specialty_name in set(CONDITION_TO_SPECIALTY.values()):
        if specialty_name.lower() in message_lower:
            found_specialty = specialty_name
            break
    
    # If no exact specialty name was found, check for conditions
    if not found_specialty:
        for condition, specialty in CONDITION_TO_SPECIALTY.items():
            if condition in message_lower:
                found_specialty = specialty
                break
    
    # If we found a specialty and it's a doctor-related query
    if found_specialty and any(term in message_lower for term in ["doctor", "specialist", "bác sĩ", "chuyên gia", "bác sỹ", "khám", "chữa"]):
        return get_doctors_by_specialty(found_specialty, language)
    
    # Check for greetings
    if any(greeting in message_lower for greeting in ["hello", "hi", "hey", "greetings", "xin chào", "chào", "xin chao", "chao"]):
        return random.choice(GREETINGS)
    
    # Check for appointment-related queries
    if any(term in message_lower for term in ["appointment", "schedule", "book", "visit", "doctor", "lịch hẹn", "đặt lịch", "hẹn gặp", "đặt khám", "khám bệnh"]):
        return random.choice(APPOINTMENT_RESPONSES)
    
    # Check for symptom-related queries
    for symptom, response in MEDICAL_SYMPTOMS.items():
        if symptom in message_lower:
            return response
    
    # Check for medication or prescription queries
    if any(term in message_lower for term in ["medicine", "medication", "prescription", "drug", "pharmacy", 
                                             "thuốc", "đơn thuốc", "kê đơn", "nhà thuốc", "dược phẩm"]):
        if language == 'vi':
            return "Về các vấn đề liên quan đến thuốc hoặc đơn thuốc, vui lòng kiểm tra phần Nhà thuốc trong trang điều khiển của bạn hoặc tham khảo ý kiến của bác sĩ."
        else:
            return "For medication or prescription inquiries, please check the Pharmacy section in your dashboard or consult with your doctor."
    
    # Check for test-related queries
    if any(term in message_lower for term in ["test", "lab", "blood", "urine", "sample", 
                                             "xét nghiệm", "phòng thí nghiệm", "máu", "nước tiểu", "mẫu"]):
        if language == 'vi':
            return "Để biết thông tin về xét nghiệm, vui lòng kiểm tra phần Xét nghiệm trong trang điều khiển của bạn hoặc tham khảo ý kiến của bác sĩ."
        else:
            return "For lab test information, please check the Lab Tests section in your dashboard or consult with your doctor."
    
    # Check for billing or payment queries
    if any(term in message_lower for term in ["bill", "payment", "insurance", "cost", "pay", 
                                             "hóa đơn", "thanh toán", "bảo hiểm", "chi phí", "trả tiền"]):
        if language == 'vi':
            return "Về các vấn đề thanh toán, vui lòng truy cập phần Thanh toán & Hóa đơn trong trang điều khiển của bạn hoặc liên hệ với bộ phận thanh toán của chúng tôi."
        else:
            return "For billing inquiries, please visit the Billing & Payment section in your dashboard or contact our billing department."
    
    # Check for profile-related queries
    if any(term in message_lower for term in ["profile", "account", "information", "details", "password", 
                                             "hồ sơ", "tài khoản", "thông tin", "chi tiết", "mật khẩu"]):
        if language == 'vi':
            return "Bạn có thể cập nhật thông tin hồ sơ của mình trong phần Chỉnh sửa hồ sơ trên trang điều khiển của bạn."
        else:
            return "You can update your profile information in the Edit Profile section of your dashboard."
    
    # Default responses
    return random.choice(GENERAL_RESPONSES)
