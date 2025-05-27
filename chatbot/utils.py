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
    "đau đầu": "Đau đầu có thể do nhiều nguyên nhân như căng thẳng, mất nước, thiếu ngủ, hoặc mỏi mắt. Các loại đau đầu phổ biến:\n• Đau đầu căng thẳng: Đau âm ỉ, cảm giác bị siết chặt quanh đầu\n• Đau nửa đầu (migraine): Đau nhói một bên, kèm buồn nôn, nhạy cảm với ánh sáng\n• Đau đầu cụm: Đau dữ dội một bên, thường quanh mắt\n\nNên đi khám ngay nếu đau đầu dữ dội đột ngột, kèm sốt cao, cứng cổ, hoặc rối loạn ý thức.",
    
    "sốt": "Sốt là dấu hiệu cơ thể đang chống lại nhiễm trùng. Phân loại mức độ sốt:\n• Sốt nhẹ: 37.5°C - 38°C\n• Sốt vừa: 38°C - 39°C\n• Sốt cao: 39°C - 41°C\n\nCách xử trí: nghỉ ngơi, uống nhiều nước, dùng thuốc hạ sốt (paracetamol), chườm mát. Cần đi khám ngay nếu sốt cao kéo dài, kèm phát ban, đau đầu dữ dội, hoặc khó thở.",
    
    "ho": "Ho là phản xạ bảo vệ đường thở, có thể do nhiều nguyên nhân:\n• Ho mới xuất hiện: Thường do viêm họng, cảm lạnh, cúm\n• Ho kèm đờm: Có thể do viêm phế quản, viêm phổi\n• Ho khan kéo dài: Có thể do dị ứng, hen suyễn, trào ngược dạ dày\n• Ho có máu: Cần đi khám ngay\n\nĐiều trị tùy nguyên nhân, có thể dùng siro ho, thuốc giảm ho hoặc long đờm. Cần đi khám nếu ho kéo dài trên 2 tuần, ho ra máu, hoặc khó thở.",
    "đau tim": "Đau tim có thể là dấu hiệu của bệnh tim mạch nghiêm trọng. Các triệu chứng cần chú ý:\n• Đau thắt, nặng hoặc bó chặt ở giữa ngực\n• Đau lan ra cánh tay trái, hàm, cổ\n• Khó thở, vã mồ hôi, buồn nôn\n• Cảm giác hồi hộp, lo lắng\n\nCẦN CẤP CỨU NGAY nếu đau ngực dữ dội đột ngột, kéo dài >15 phút và không giảm khi nghỉ ngơi.",
    "khó thở": "Khó thở có thể do bệnh phổi, tim, thiếu máu hoặc lo âu. Dấu hiệu cần chú ý:\n• Khó thở đột ngột hoặc nặng dần\n• Kèm đau ngực hoặc tim đập nhanh\n• Không thể nói trọn câu do thiếu hơi\n• Môi hoặc móng tay tím\n\nCẦN CẤP CỨU NGAY nếu khó thở dữ dội, đột ngột hoặc kèm theo đau ngực.",
    
    "đau bụng": "Đau bụng có thể do nhiều nguyên nhân từ đơn giản đến nghiêm trọng. Đặc điểm cần chú ý:\n• Vị trí đau (trên/dưới rốn, bên phải/trái)\n• Tính chất đau (âm ỉ, dữ dội, từng cơn)\n• Các triệu chứng kèm theo (nôn, tiêu chảy, sốt)\n\nNên đi khám ngay nếu đau dữ dội đột ngột, kèm sốt cao, nôn ra máu, phân đen, hoặc đau nhiều ở hố chậu phải.",
    
    "đau ngực": "Đau ngực là triệu chứng cần được quan tâm đặc biệt, có thể liên quan đến tim hoặc không. Đặc điểm đau ngực nguy hiểm:\n• Đau thắt, nặng hoặc bó chặt ở giữa ngực\n• Đau lan ra cánh tay trái, hàm, cổ\n• Kèm khó thở, vã mồ hôi, buồn nôn\n\nCẦN CẤP CỨU NGAY nếu đau ngực dữ dội đột ngột, kéo dài >15 phút và không giảm khi nghỉ ngơi.",
    
    "đau lưng": "Đau lưng thường do các vấn đề cơ xương khớp như căng cơ, thoái hóa đốt sống, thoát vị đĩa đệm. Biểu hiện cần chú ý:\n• Vị trí đau (lưng trên, lưng dưới)\n• Đau lan xuống chân hoặc không\n• Đau tăng khi vận động hoặc nghỉ ngơi\n\nĐi khám ngay nếu đau dữ dội sau chấn thương, kèm tê bì chân, mất kiểm soát đại tiểu tiện, hoặc sốt cao.",
    
    "mệt mỏi": "Mệt mỏi kéo dài có thể do nhiều nguyên nhân như:\n• Thiếu ngủ, căng thẳng kéo dài\n• Thiếu máu, suy giáp, tiểu đường\n• Trầm cảm, lo âu\n• Viêm nhiễm mạn tính, ung thư\n\nCách cải thiện: ngủ đủ 7-8h/ngày, tập thể dục đều đặn, điều chỉnh chế độ ăn cân bằng. Nên đi khám nếu mệt mỏi kéo dài trên 2 tuần dù đã nghỉ ngơi đầy đủ.",
    
    "chóng mặt": "Chóng mặt là cảm giác quay cuồng, mất thăng bằng hoặc choáng váng. Nguyên nhân phổ biến:\n• Rối loạn tiền đình (viêm dây thần kinh tiền đình)\n• Thiếu máu não thoáng qua, hạ đường huyết\n• Tác dụng phụ của thuốc\n• Mất nước, hạ huyết áp thế đứng\n\nCần đi khám ngay nếu chóng mặt đột ngột dữ dội, kèm theo đau đầu, yếu liệt nửa người, rối loạn nói, hoặc ngất.",
    
    "nôn": "Nôn là phản xạ đẩy thức ăn từ dạ dày ra ngoài, có thể do:\n• Viêm dạ dày, ngộ độc thực phẩm\n• Say tàu xe, rối loạn tiền đình\n• Tác dụng phụ của thuốc\n• Các vấn đề thần kinh, tăng áp lực nội sọ\n\nĐiều trị: bù nước và điện giải, ăn nhẹ, dùng thuốc chống nôn. Cần đi khám ngay nếu nôn ra máu, nôn kèm đau đầu dữ dội, nôn liên tục không cầm được, hoặc nôn ở trẻ sơ sinh.",
    
    "tiêu chảy": "Tiêu chảy là đi phân lỏng, nhiều lần trong ngày. Nguyên nhân thường gặp:\n• Nhiễm khuẩn, virus hoặc ký sinh trùng\n• Ngộ độc thực phẩm\n• Tác dụng phụ của thuốc (đặc biệt là kháng sinh)\n• Bệnh đường ruột mạn tính\n\nCần bù nước và điện giải là việc quan trọng nhất. Đi khám ngay nếu tiêu chảy kéo dài trên 3 ngày, phân có máu, sốt cao, hoặc có dấu hiệu mất nước nghiêm trọng.",
    
    "táo bón": "Táo bón là tình trạng đi đại tiện khó khăn, ít hơn 3 lần/tuần, phân khô cứng. Nguyên nhân phổ biến:\n• Ăn ít chất xơ, uống ít nước\n• Ít vận động, thay đổi thói quen sinh hoạt\n• Tác dụng phụ của thuốc\n• Hội chứng ruột kích thích\n\nCách cải thiện: tăng cường chất xơ (rau, trái cây, ngũ cốc nguyên hạt), uống đủ nước, vận động thường xuyên. Đi khám nếu táo bón kéo dài hoặc kèm đau bụng, sút cân, phân có máu.",
    
    "sốt xuất huyết": "Sốt xuất huyết là bệnh truyền nhiễm do virus Dengue gây ra, qua trung gian muỗi Aedes. Triệu chứng điển hình:\n• Sốt cao đột ngột 2-7 ngày\n• Đau đầu dữ dội, đau sau nhãn cầu\n• Đau cơ, đau khớp, đau xương\n• Phát ban, xuất huyết dưới da, chảy máu nướu, chảy máu mũi\n\nCẦN ĐI KHÁM NGAY nếu nghi ngờ sốt xuất huyết, đặc biệt khi sốt giảm mà tình trạng chung xấu đi, đau bụng dữ dội, nôn ói liên tục.",
    
    "cảm lạnh": "Cảm lạnh là bệnh nhiễm virus thường gặp, với các triệu chứng:\n• Nghẹt mũi, sổ mũi, hắt hơi\n• Đau họng, ho nhẹ\n• Sốt nhẹ hoặc không sốt\n• Mệt mỏi nhẹ\n\nBệnh thường tự khỏi sau 7-10 ngày. Điều trị: nghỉ ngơi, uống nhiều nước, dùng thuốc giảm đau hạ sốt nếu cần. Đi khám nếu triệu chứng kéo dài trên 10 ngày, sốt cao, khó thở, hoặc đau tai.",
    
    "cúm": "Cúm là bệnh nhiễm virus cúm, thường nặng hơn cảm lạnh. Triệu chứng điển hình:\n• Sốt cao đột ngột (38-40°C)\n• Đau nhức cơ thể, đặc biệt cơ lưng và chân\n• Đau đầu dữ dội\n• Mệt mỏi, kiệt sức\n• Ho khan, đau họng\n\nĐiều trị: nghỉ ngơi, uống nhiều nước, dùng thuốc hạ sốt giảm đau. Thuốc kháng virus có thể được dùng trong 48h đầu. Đi khám nếu sốt cao kéo dài, khó thở, hoặc triệu chứng nặng lên sau vài ngày đầu.",
    
    "dị ứng": "Dị ứng là phản ứng quá mức của hệ miễn dịch với chất lạ (dị nguyên). Triệu chứng phổ biến:\n• Hắt hơi, sổ mũi, ngứa mũi họng\n• Ngứa, đỏ, sưng mắt\n• Phát ban, ngứa da\n• Khó thở, thở khò khè (trong trường hợp nặng)\n\nĐiều trị: tránh tiếp xúc với dị nguyên, dùng thuốc kháng histamine. CẦN CẤP CỨU NGAY nếu có phản ứng dị ứng nặng với khó thở, sưng môi/lưỡi, tụt huyết áp."
}

# Vietnamese appointment responses
APPOINTMENT_RESPONSES_VI = [
    "Bạn có thể đặt lịch hẹn thông qua mục 'Đặt lịch hẹn' trong trang điều khiển của bệnh nhân.",
    "Để lên lịch hẹn, vui lòng sử dụng tính năng đặt lịch hẹn trong tài khoản của bạn.",
    "Lịch hẹn có thể được đặt trực tuyến thông qua cổng thông tin bệnh nhân hoặc bằng cách gọi điện đến văn phòng của chúng tôi.",
]

# English appointment responses
APPOINTMENT_RESPONSES_EN = [
    "You can book an appointment through the 'Book Appointment' section in your patient dashboard.",
    "To schedule an appointment, please use the appointment booking feature in your account.",
    "Appointments can be booked online through your patient portal or by calling our office.",
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

# Add a new dictionary for detailed health information responses in Vietnamese
HEALTH_INFO_VI = {
    "đau thắt ngực": "Đau thắt ngực (hay còn gọi là thiếu máu cơ tim) là tình trạng đau ngực do tim không nhận đủ máu giàu oxy. Triệu chứng thường gặp bao gồm:\n• Cảm giác đau, nặng, tức, hoặc bó chặt ở ngực\n• Đau lan ra cánh tay trái, cổ, hàm, vai hoặc lưng\n• Khó thở, buồn nôn, đổ mồ hôi\n\nNếu bạn gặp những triệu chứng này, hãy đi khám bác sĩ Tim mạch ngay lập tức. Trong trường hợp đau dữ dội kéo dài trên 5 phút, hãy gọi cấp cứu ngay.",
    
    "nhồi máu cơ tim": "Nhồi máu cơ tim (đau tim) là tình trạng khẩn cấp khi dòng máu đến tim bị chặn đột ngột, gây tổn thương cho cơ tim. Các dấu hiệu bao gồm:\n• Đau ngực dữ dội, cảm giác nặng nề hoặc bó chặt kéo dài\n• Đau lan đến vai, cánh tay, lưng, cổ hoặc hàm\n• Khó thở, buồn nôn, chóng mặt\n• Đổ mồ hôi lạnh\n\nĐây là tình trạng CẤP CỨU - hãy gọi ngay xe cấp cứu (115) và không nên tự lái xe đến bệnh viện.",
    
    "cao huyết áp": "Cao huyết áp (tăng huyết áp) là tình trạng áp lực máu lên thành động mạch quá cao. Bệnh thường không có triệu chứng rõ ràng nhưng có thể gây:\n• Đau đầu\n• Chóng mặt\n• Mờ mắt\n• Khó thở\n\nTăng huyết áp kéo dài không điều trị có thể dẫn đến đột quỵ, đau tim và suy thận. Hãy đi khám bác sĩ Tim mạch để được tư vấn điều trị.",
    
    "đột quỵ": "Đột quỵ xảy ra khi nguồn cung cấp máu đến não bị gián đoạn, gây tổn thương não. Dấu hiệu nhận biết đột quỵ theo nguyên tắc F.A.S.T:\n• Face (Mặt): Mặt bị méo, cười không đều\n• Arms (Tay): Yếu hoặc tê liệt một bên tay\n• Speech (Nói): Nói ngọng, khó phát âm\n• Time (Thời gian): Gọi cấp cứu ngay lập tức\n\nĐột quỵ là tình trạng CẤP CỨU - hãy gọi xe cấp cứu (115) ngay lập tức.",
    
    "suy tim": "Suy tim là tình trạng tim không thể bơm đủ máu để đáp ứng nhu cầu của cơ thể. Triệu chứng thường gặp:\n• Khó thở, đặc biệt khi hoạt động hoặc nằm xuống\n• Mệt mỏi, yếu ớt\n• Phù chân, mắt cá chân, bụng\n• Tim đập nhanh hoặc không đều\n\nNếu bạn có các triệu chứng này, hãy đi khám bác sĩ Tim mạch sớm."
}

# Add English versions of the detailed health information
HEALTH_INFO_EN = {
    "angina": "Angina pectoris is chest pain caused by reduced blood flow to the heart muscles. Common symptoms include:\n• Chest pain, pressure, or tightness\n• Pain radiating to your left arm, neck, jaw, shoulder or back\n• Shortness of breath, nausea, sweating\n\nIf you experience these symptoms, consult a cardiologist immediately. If pain is severe and lasts more than 5 minutes, seek emergency care.",
    
    "heart attack": "A heart attack occurs when blood flow to part of the heart is suddenly blocked, causing damage to the heart muscle. Signs include:\n• Severe chest pain, pressure or tightness that persists\n• Pain spreading to shoulders, arms, back, neck or jaw\n• Shortness of breath, nausea, dizziness\n• Cold sweat\n\nThis is an EMERGENCY - call an ambulance immediately and don't drive yourself to the hospital.",
    
    "high blood pressure": "High blood pressure (hypertension) is when the pressure of blood against artery walls is too high. It often has no obvious symptoms but may cause:\n• Headaches\n• Dizziness\n• Blurred vision\n• Shortness of breath\n\nUntreated high blood pressure can lead to stroke, heart attack, and kidney failure. Consult a cardiologist for treatment advice.",
    
    "stroke": "A stroke occurs when blood supply to the brain is interrupted, causing brain damage. Recognize stroke using the F.A.S.T principle:\n• Face: Facial drooping\n• Arms: Arm weakness\n• Speech: Speech difficulties\n• Time: Time to call emergency services\n\nStroke is an EMERGENCY - call an ambulance immediately.",
    
    "heart failure": "Heart failure is a condition where your heart can't pump enough blood to meet your body's needs. Common symptoms:\n• Shortness of breath, especially during activity or lying down\n• Fatigue and weakness\n• Swelling in legs, ankles, or abdomen\n• Rapid or irregular heartbeat\n\nIf you have these symptoms, consult a cardiologist promptly."
}

# Add detailed information about abdominal pain to Vietnamese health info
HEALTH_INFO_VI.update({
    "đau bụng": "Đau bụng là triệu chứng phổ biến có thể liên quan đến nhiều bệnh lý khác nhau. Dựa trên vị trí đau:\n• Đau bụng trên: Có thể liên quan đến dạ dày, gan, túi mật, tụy\n• Đau bụng dưới: Có thể liên quan đến ruột, phụ khoa (ở nữ), tiết niệu\n• Đau quanh rốn: Thường gặp trong viêm ruột thừa giai đoạn đầu\n\nTùy thuộc vào tính chất đau và triệu chứng kèm theo, bạn nên thăm khám bác sĩ chuyên khoa Tiêu hóa hoặc Ngoại khoa.",
    
    "đau dạ dày": "Đau dạ dày thường biểu hiện như cảm giác đau, nóng rát hoặc khó chịu ở vùng thượng vị (bụng trên). Nguyên nhân phổ biến bao gồm:\n• Viêm loét dạ dày, tá tràng\n• Trào ngược dạ dày thực quản\n• Nhiễm khuẩn Helicobacter pylori\n• Stress và lo âu\n\nNếu đau dạ dày kéo dài hoặc tái phát, kèm theo nôn ra máu hoặc phân đen, hãy đi khám bác sĩ Tiêu hóa ngay lập tức.",
    
    "táo bón": "Táo bón là tình trạng đi đại tiện khó khăn, ít hơn 3 lần/tuần, phân khô cứng. Nguyên nhân phổ biến:\n• Ăn ít chất xơ, uống ít nước\n• Ít vận động\n• Thay đổi thói quen sinh hoạt\n• Một số loại thuốc\n• Bệnh lý đường tiêu hóa\n\nĐể cải thiện: tăng cường chất xơ, uống đủ nước, vận động thường xuyên. Nếu táo bón kéo dài hoặc kèm đau bụng, chảy máu, hãy đi khám bác sĩ Tiêu hóa.",
    
    "tiêu chảy": "Tiêu chảy là tình trạng đi phân lỏng, nhiều lần trong ngày. Nguyên nhân thường gặp:\n• Nhiễm khuẩn, virus hoặc ký sinh trùng\n• Ngộ độc thực phẩm\n• Dị ứng thực phẩm\n• Sử dụng kháng sinh\n• Bệnh đường ruột mạn tính\n\nTiêu chảy cấp thường tự khỏi sau 2-3 ngày. Cần bù nước và điện giải. Đi khám bác sĩ nếu tiêu chảy kéo dài trên 3 ngày, kèm sốt cao, phân có máu hoặc mất nước nghiêm trọng.",
    
    "viêm ruột thừa": "Viêm ruột thừa là tình trạng khẩn cấp, thường bắt đầu với đau quanh rốn sau dồn xuống hố chậu phải. Dấu hiệu nhận biết:\n• Đau bụng dữ dội hố chậu phải\n• Buồn nôn và nôn\n• Sốt nhẹ\n• Đau tăng khi ho, đi lại\n• Chán ăn\n\nĐây là tình trạng CẤP CỨU - cần đến bệnh viện ngay để được chẩn đoán và phẫu thuật kịp thời nếu cần thiết."
})

# Add English versions of abdominal pain information
HEALTH_INFO_EN.update({
    "abdominal pain": "Abdominal pain is a common symptom that can be related to various conditions. Based on location:\n• Upper abdomen: May involve stomach, liver, gallbladder, pancreas\n• Lower abdomen: May involve intestines, gynecological issues (in women), urinary tract\n• Around navel: Often seen in early appendicitis\n\nDepending on the nature of pain and accompanying symptoms, you should consult a Gastroenterologist or Surgeon.",
    
    "stomach pain": "Stomach pain typically manifests as pain, burning, or discomfort in the epigastric region (upper abdomen). Common causes include:\n• Gastritis or peptic ulcers\n• Gastroesophageal reflux disease (GERD)\n• Helicobacter pylori infection\n• Stress and anxiety\n\nIf stomach pain persists or recurs, especially with vomiting blood or black stools, see a Gastroenterologist immediately.",
    
    "constipation": "Constipation is a condition of difficult bowel movements, fewer than 3 times per week, with hard dry stools. Common causes:\n• Low fiber diet, inadequate water intake\n• Lack of physical activity\n• Changes in routine\n• Certain medications\n• Digestive tract disorders\n\nTo improve: increase fiber, drink more water, exercise regularly. If constipation persists or is accompanied by abdominal pain or bleeding, consult a Gastroenterologist.",
    
    "diarrhea": "Diarrhea is a condition of loose, watery stools occurring multiple times a day. Common causes:\n• Bacterial, viral, or parasitic infections\n• Food poisoning\n• Food allergies\n• Antibiotic use\n• Chronic intestinal disorders\n\nAcute diarrhea usually resolves within 2-3 days. Fluid and electrolyte replacement is important. See a doctor if diarrhea lasts more than 3 days, is accompanied by high fever, bloody stools, or severe dehydration.",
    
    "appendicitis": "Appendicitis is an emergency condition, typically starting with pain around the navel that moves to the lower right abdomen. Signs include:\n• Severe pain in the lower right abdomen\n• Nausea and vomiting\n• Low-grade fever\n• Pain that worsens with coughing or walking\n• Loss of appetite\n\nThis is an EMERGENCY - go to the hospital immediately for diagnosis and timely surgery if needed."
})

# Add orthopedic conditions to Vietnamese health info
HEALTH_INFO_VI.update({
    "thoái hóa khớp": "Thoái hóa khớp là tình trạng sụn khớp bị bào mòn dần theo thời gian. Triệu chứng thường gặp:\n• Đau khớp, đặc biệt khi vận động hoặc sau vận động\n• Cứng khớp, đặc biệt vào buổi sáng hoặc sau thời gian nghỉ ngơi\n• Tiếng kêu lục khục khi cử động khớp\n• Sưng và giảm biên độ vận động khớp\n\nĐiều trị bao gồm thuốc giảm đau, vật lý trị liệu và trong một số trường hợp nghiêm trọng có thể cần phẫu thuật thay khớp. Nên thăm khám bác sĩ chuyên khoa Xương khớp để được tư vấn phù hợp.",
    
    "viêm khớp dạng thấp": "Viêm khớp dạng thấp là bệnh tự miễn gây viêm màng hoạt dịch của khớp. Đặc điểm nhận biết:\n• Đau, sưng và nóng ở nhiều khớp, thường đối xứng hai bên cơ thể\n• Cứng khớp vào buổi sáng kéo dài trên 30 phút\n• Mệt mỏi, sốt nhẹ và giảm cân\n• Các nốt dưới da (nốt thấp)\n\nĐây là bệnh mạn tính cần được điều trị sớm để ngăn ngừa biến dạng khớp. Hãy tham khảo ý kiến bác sĩ chuyên khoa Xương khớp hoặc Cơ xương khớp.",
    
    "bệnh gút": "Bệnh gút (gout) là do tình trạng tăng acid uric trong máu gây lắng đọng tinh thể urat tại các khớp. Biểu hiện điển hình:\n• Đau khớp đột ngột, dữ dội, thường bắt đầu ở ngón chân cái\n• Khớp sưng, đỏ, nóng và rất đau khi chạm vào\n• Cơn đau thường xảy ra vào ban đêm và có thể kéo dài 3-10 ngày\n• Sốt nhẹ trong cơn cấp\n\nĐiều trị bao gồm thuốc chống viêm trong giai đoạn cấp và thuốc hạ acid uric lâu dài. Chế độ ăn hạn chế purin cũng rất quan trọng.",
    
    "loãng xương": "Loãng xương là tình trạng mật độ xương giảm, làm xương trở nên xốp và dễ gãy. Dấu hiệu thường gặp:\n• Không có triệu chứng ban đầu, thường phát hiện khi bị gãy xương\n• Đau lưng do gãy xẹp đốt sống\n• Giảm chiều cao theo thời gian\n• Tư thế lưng còng\n\nPhụ nữ sau mãn kinh và người cao tuổi có nguy cơ cao nhất. Điều trị bao gồm bổ sung canxi, vitamin D, tập thể dục phù hợp và thuốc chống hủy xương khi cần thiết.",
    
    "đau lưng": "Đau lưng có thể do nhiều nguyên nhân khác nhau, từ căng cơ đến thoát vị đĩa đệm. Triệu chứng phổ biến:\n• Đau âm ỉ hoặc nhói ở vùng lưng\n• Cứng và khó khăn khi cử động\n• Đau lan xuống chân (nếu liên quan đến dây thần kinh)\n• Đau tăng khi vận động và giảm khi nghỉ ngơi\n\nĐiều trị phụ thuộc vào nguyên nhân, có thể bao gồm nghỉ ngơi, vật lý trị liệu, thuốc giảm đau. Nếu đau kéo dài trên 6 tuần hoặc kèm theo tê chân, yếu cơ, hãy đi khám bác sĩ Xương khớp hoặc Thần kinh.",
    
    "thoát vị đĩa đệm": "Thoát vị đĩa đệm xảy ra khi phần mềm ở giữa các đốt sống (đĩa đệm) bị đẩy ra ngoài và chèn ép dây thần kinh. Biểu hiện chính:\n• Đau lưng dưới hoặc đau cổ tùy vị trí thoát vị\n• Đau lan theo đường đi của dây thần kinh (xuống chân hoặc ra tay)\n• Tê, ngứa ran hoặc yếu ở chân/tay\n• Đau tăng khi ho, hắt hơi hoặc ngồi lâu\n\nCần thăm khám bác sĩ chuyên khoa Xương khớp hoặc Thần kinh để được chẩn đoán và điều trị phù hợp."
})

# Add orthopedic conditions to English health info
HEALTH_INFO_EN.update({
    "osteoarthritis": "Osteoarthritis is a condition where the cartilage in joints wears down over time. Common symptoms include:\n• Joint pain, especially during or after movement\n• Joint stiffness, particularly in the morning or after periods of rest\n• Grating sensation when moving the joint\n• Swelling and reduced range of motion\n\nTreatment includes pain medication, physical therapy, and in severe cases, joint replacement surgery. Consult with an Orthopedic specialist for appropriate advice.",
    
    "rheumatoid arthritis": "Rheumatoid arthritis is an autoimmune disease causing inflammation of the synovial membrane of joints. Identifying features:\n• Pain, swelling, and warmth in multiple joints, usually symmetrically on both sides of the body\n• Morning stiffness lasting more than 30 minutes\n• Fatigue, low-grade fever, and weight loss\n• Subcutaneous nodules (rheumatoid nodules)\n\nThis is a chronic condition requiring early treatment to prevent joint deformity. Consult with a Rheumatologist or Orthopedic specialist.",
    
    "gout": "Gout is caused by elevated uric acid levels in the blood, resulting in urate crystal deposits in joints. Typical manifestations:\n• Sudden, severe joint pain, often starting in the big toe\n• Joint swelling, redness, heat, and extreme tenderness\n• Pain typically occurs at night and may last 3-10 days\n• Mild fever during acute attacks\n\nTreatment includes anti-inflammatory medications for acute phases and uric acid-lowering drugs for long-term management. A low-purine diet is also important.",
    
    "osteoporosis": "Osteoporosis is a condition where bone density decreases, making bones porous and prone to fractures. Common signs:\n• No initial symptoms, often discovered after a fracture occurs\n• Back pain due to vertebral compression fractures\n• Loss of height over time\n• Stooped posture\n\nPostmenopausal women and the elderly are at highest risk. Treatment includes calcium and vitamin D supplements, appropriate exercise, and anti-resorptive medications when necessary.",
    
    "back pain": "Back pain can have various causes, from muscle strain to herniated discs. Common symptoms:\n• Dull or sharp pain in the back region\n• Stiffness and difficulty moving\n• Pain radiating down the leg (if nerve-related)\n• Pain that worsens with movement and improves with rest\n\nTreatment depends on the cause and may include rest, physical therapy, and pain medication. If pain persists for more than 6 weeks or is accompanied by leg numbness or muscle weakness, consult an Orthopedic or Neurological specialist.",
    
    "herniated disc": "Herniated disc occurs when the soft center of a spinal disc pushes out and compresses a nerve. Main symptoms:\n• Lower back or neck pain depending on the location\n• Pain radiating along the nerve pathway (down leg or arm)\n• Numbness, tingling, or weakness in leg/arm\n• Pain that increases with coughing, sneezing, or sitting\n\nConsult with an Orthopedic or Neurological specialist for proper diagnosis and treatment."
})

# Enhance chest pain information in Vietnamese health info
HEALTH_INFO_VI.update({
    "đau ngực": "Đau ngực có thể do nhiều nguyên nhân khác nhau, từ vấn đề tim mạch đến các vấn đề không liên quan đến tim. Dấu hiệu cần chú ý:\n• Đau thắt, nặng, hoặc cảm giác bó chặt ở ngực\n• Đau lan tỏa ra cánh tay trái, hàm, cổ, lưng\n• Kèm theo khó thở, vã mồ hôi, buồn nôn\n• Đau tăng khi gắng sức và giảm khi nghỉ ngơi\n\nCÁC DẤU HIỆU NGUY HIỂM cần đến cấp cứu ngay:\n• Đau ngực dữ dội đột ngột\n• Đau kèm khó thở nặng, vã mồ hôi, chóng mặt\n• Đau lan đến cánh tay trái, hàm dưới\n• Đau kéo dài trên 15 phút không giảm khi nghỉ ngơi\n\nNên thăm khám bác sĩ Tim mạch để được chẩn đoán và điều trị phù hợp.",
    
    "đau ngực không do tim": "Đau ngực không do tim có thể do nhiều nguyên nhân như:\n• Viêm phế quản, viêm phổi (đau khi hít thở sâu, kèm ho)\n• Viêm thực quản, trào ngược dạ dày (đau rát sau xương ức, tăng sau ăn)\n• Viêm sụn sườn (đau khi ấn vào thành ngực)\n• Lo âu, căng thẳng (thường kèm theo hồi hộp, khó thở)\n• Rối loạn cơ xương (đau thay đổi khi cử động, vặn người)\n\nCác dấu hiệu giúp phân biệt với đau ngực do tim:\n• Thường đau nhói hoặc đau âm ỉ khu trú\n• Đau thay đổi khi thay đổi tư thế hoặc hít thở\n• Có thể tái tạo cơn đau khi ấn vào vùng đau\n• Thường kéo dài nhiều giờ hoặc nhiều ngày\n\nTuy nhiên, nếu không chắc chắn, hãy đi khám để được chẩn đoán chính xác.",
    
    "đau lưng cấp tính": "Đau lưng cấp tính thường xuất hiện đột ngột và kéo dài dưới 6 tuần. Nguyên nhân phổ biến:\n• Căng cơ và dây chằng (do nâng vật nặng hoặc cử động sai tư thế)\n• Chấn thương (ngã, tai nạn)\n• Thoát vị đĩa đệm cấp tính\n• Gãy xẹp đốt sống (ở người có loãng xương)\n\nCác dấu hiệu cần đi cấp cứu ngay:\n• Đau dữ dội không giảm khi nghỉ ngơi\n• Đau kèm theo tê bì hoặc yếu hai chân\n• Mất kiểm soát đại tiểu tiện\n• Đau sau chấn thương nặng\n• Sốt cao kèm đau lưng\n\nĐiều trị: nghỉ ngơi ngắn (1-2 ngày), thuốc giảm đau, chườm nóng/lạnh, và dần dần trở lại hoạt động bình thường.",
    
    "đau lưng mạn tính": "Đau lưng mạn tính kéo dài trên 12 tuần dù đã được điều trị ban đầu. Nguyên nhân thường gặp:\n• Thoái hóa cột sống (thường ở người trên 40 tuổi)\n• Thoát vị đĩa đệm mạn tính\n• Hẹp ống sống\n• Vẹo cột sống hoặc dị dạng cột sống khác\n• Viêm cột sống dính khớp\n• Đau lưng do căng thẳng, tâm lý\n\nĐặc điểm của đau lưng mạn tính:\n• Đau âm ỉ, có thể tăng giảm theo thời gian\n• Thường nặng hơn vào buổi sáng hoặc cuối ngày\n• Giảm khả năng vận động và ảnh hưởng chất lượng cuộc sống\n• Có thể kèm theo rối loạn giấc ngủ, mệt mỏi, trầm cảm\n\nĐiều trị đòi hỏi phương pháp đa mô thức: vật lý trị liệu, tập luyện, kiểm soát cân nặng, và đôi khi can thiệp ngoại khoa.",
    
    "đau thần kinh tọa": "Đau thần kinh tọa (đau dây thần kinh hông to) là tình trạng đau dọc theo đường đi của dây thần kinh tọa, từ lưng dưới xuống mông và chạy dọc xuống chân. Đặc điểm:\n• Đau nhói như điện giật, rát bỏng hoặc đau nhức\n• Đau lan từ lưng dưới xuống mông và xuống sau đùi, bắp chân\n• Thường chỉ ảnh hưởng một bên cơ thể\n• Tê bì, ngứa ran hoặc yếu ở chân bị ảnh hưởng\n• Đau tăng khi ngồi lâu, ho, hắt hơi\n\nNguyên nhân thường do thoát vị đĩa đệm, hẹp ống sống, hoặc hội chứng cơ hình lê chèn ép dây thần kinh tọa. Điều trị bao gồm thuốc giảm đau, vật lý trị liệu, và trong trường hợp nặng có thể cần phẫu thuật."
})

# Enhance chest pain information in English health info
HEALTH_INFO_EN.update({
    "chest pain": "Chest pain can have various causes, from cardiovascular issues to non-cardiac problems. Signs to watch for:\n• Squeezing, heaviness, or tightness in the chest\n• Pain radiating to the left arm, jaw, neck, back\n• Accompanied by shortness of breath, sweating, nausea\n• Pain increases with exertion and decreases with rest\n\nDANGER SIGNS requiring immediate emergency care:\n• Sudden severe chest pain\n• Pain with severe shortness of breath, sweating, dizziness\n• Pain radiating to the left arm, lower jaw\n• Pain lasting more than 15 minutes not relieved by rest\n\nYou should consult a Cardiologist for proper diagnosis and treatment.",
    
    "non-cardiac chest pain": "Non-cardiac chest pain can have various causes such as:\n• Bronchitis, pneumonia (pain when breathing deeply, with cough)\n• Esophagitis, acid reflux (burning pain behind breastbone, worse after eating)\n• Costochondritis (pain when pressing on chest wall)\n• Anxiety, stress (often with palpitations, shortness of breath)\n• Musculoskeletal disorders (pain changes with movement, twisting)\n\nSigns that help differentiate from cardiac chest pain:\n• Usually sharp or localized dull pain\n• Pain changes with position or breathing\n• Pain can be reproduced by pressing on the painful area\n• Often lasts for hours or days\n\nHowever, if uncertain, seek medical evaluation for accurate diagnosis.",
    
    "acute back pain": "Acute back pain typically appears suddenly and lasts less than 6 weeks. Common causes:\n• Muscle and ligament strain (from lifting heavy objects or improper movement)\n• Trauma (falls, accidents)\n• Acute herniated disc\n• Vertebral compression fractures (in people with osteoporosis)\n\nSigns requiring immediate emergency care:\n• Severe pain not relieved by rest\n• Pain with numbness or weakness in both legs\n• Loss of bladder or bowel control\n• Pain following severe trauma\n• High fever with back pain\n\nTreatment: short rest (1-2 days), pain medication, hot/cold compresses, and gradual return to normal activity.",
    
    "chronic back pain": "Chronic back pain persists for more than 12 weeks despite initial treatment. Common causes:\n• Spinal degeneration (typically in people over 40)\n• Chronic herniated disc\n• Spinal stenosis\n• Scoliosis or other spinal deformities\n• Ankylosing spondylitis\n• Stress-related or psychological back pain\n\nCharacteristics of chronic back pain:\n• Dull, persistent pain that may fluctuate over time\n• Often worse in the morning or late in the day\n• Reduced mobility and impact on quality of life\n• May be accompanied by sleep disturbances, fatigue, depression\n\nTreatment requires a multimodal approach: physical therapy, exercise, weight management, and sometimes surgical intervention.",
    
    "sciatica": "Sciatica is a condition involving pain along the path of the sciatic nerve, which runs from the lower back through the hips and buttocks and down each leg. Characteristics:\n• Sharp, shooting, burning, or aching pain\n• Pain radiating from the lower back to buttocks and down the back of the thigh and calf\n• Usually affects only one side of the body\n• Numbness, tingling, or weakness in the affected leg\n• Pain worsens with prolonged sitting, coughing, sneezing\n\nThe most common causes are herniated discs, spinal stenosis, or piriformis syndrome compressing the sciatic nerve. Treatment includes pain medication, physical therapy, and in severe cases, surgery may be necessary."
})

# Add more specific mappings for different types of chest and back pain
CONDITION_TO_SPECIALTY.update({
    # Vietnamese terms
    "đau ngực": "Tim mạch",  # General chest pain -> Cardiology first
    "đau ngực do tim": "Tim mạch",
    "đau thắt ngực": "Tim mạch",
    "đau ngực không do tim": "Nội khoa",  # Non-cardiac chest pain -> General internal medicine
    "trào ngược": "Tiêu hóa",  # Reflux related chest pain -> Gastroenterology
    "viêm sụn sườn": "Xương khớp",  # Costochondritis -> Orthopedics
    
    # More specific back pain terms
    "đau lưng cấp tính": "Xương khớp",
    "đau lưng mạn tính": "Xương khớp",
    "đau thần kinh tọa": "Thần kinh",  # Sciatica -> Neurology
    "hẹp ống sống": "Xương khớp",  # Spinal stenosis -> Orthopedics
    "vẹo cột sống": "Xương khớp",  # Scoliosis -> Orthopedics
    "viêm cột sống dính khớp": "Xương khớp",  # Ankylosing spondylitis -> Orthopedics
    
    # English terms
    "chest pain": "Tim mạch",  # Cardiology
    "cardiac chest pain": "Tim mạch",
    "angina pectoris": "Tim mạch",
    "non-cardiac chest pain": "Nội khoa",  # General internal medicine
    "acid reflux chest pain": "Tiêu hóa",  # Gastroenterology
    "costochondritis": "Xương khớp",  # Orthopedics
    
    "acute back pain": "Xương khớp",  # Orthopedics
    "chronic back pain": "Xương khớp",  # Orthopedics
    "sciatica": "Thần kinh",  # Neurology
    "spinal stenosis": "Xương khớp",  # Orthopedics
    "scoliosis": "Xương khớp",  # Orthopedics
    "ankylosing spondylitis": "Xương khớp",  # Orthopedics
})

# Add treatment remedies dictionaries
TREATMENT_REMEDIES_VI = {
    "đau lưng": """
Dưới đây là 14 mẹo giúp giảm đau lưng hiệu quả:

1. Nghỉ ngơi đúng cách: Nghỉ ngơi 1-2 ngày rồi hoạt động trở lại nhẹ nhàng, tránh nằm nghỉ quá lâu
2. Chườm đá hoặc chườm nóng: Chườm đá trong 48 giờ đầu, sau đó chuyển sang chườm nóng
3. Tập thể dục nhẹ nhàng: Đi bộ, bơi lội, yoga giúp tăng cường sức mạnh cơ lưng
4. Kéo giãn cơ: Các bài tập kéo giãn giúp cải thiện tính linh hoạt và giảm căng cứng
5. Giữ tư thế đúng: Duy trì tư thế thẳng lưng khi ngồi và đứng
6. Nâng vật đúng cách: Sử dụng chân thay vì lưng khi nâng vật nặng
7. Sử dụng ghế có hỗ trợ lưng: Đệm lưng hoặc ghế công thái học khi ngồi làm việc
8. Tránh giày cao gót: Đi giày đế phẳng hoặc giày hỗ trợ vòm chân
9. Giảm cân nếu thừa cân: Giảm áp lực lên cột sống
10. Massage: Massage nhẹ nhàng có thể giúp giảm căng cơ
11. Đắp cao lá thuốc: Các loại cao dán có thể giúp giảm đau tạm thời
12. Uống đủ nước: Giữ cho đĩa đệm cột sống được đủ nước
13. Sử dụng đệm nằm phù hợp: Đệm không quá cứng hoặc quá mềm
14. Thuốc giảm đau không kê đơn: Paracetamol, Ibuprofen (nên tham khảo ý kiến bác sĩ)

Nếu đau lưng kéo dài trên 6 tuần hoặc kèm theo dấu hiệu nguy hiểm như tê tay chân, mất kiểm soát đại tiểu tiện, hãy đi khám bác sĩ ngay.
""",

    "đau đầu": """
Dưới đây là các biện pháp giảm đau đầu hiệu quả:

1. Nghỉ ngơi trong phòng yên tĩnh, tối: Giảm kích thích ánh sáng và âm thanh
2. Chườm lạnh hoặc ấm: Đặt khăn lạnh lên trán với đau đầu do căng thẳng, chườm ấm với đau đầu xoang
3. Massage nhẹ: Xoa bóp nhẹ nhàng vùng thái dương, gáy và đầu
4. Uống đủ nước: Tránh mất nước là nguyên nhân phổ biến gây đau đầu
5. Hạn chế caffeine và rượu: Hai chất này có thể gây đau đầu hoặc làm nặng hơn
6. Ngủ đủ giấc: Duy trì thời gian ngủ đều đặn, đủ 7-8 tiếng mỗi ngày
7. Thả lỏng cơ thể: Thực hành thư giãn như hít thở sâu, thiền
8. Tránh các yếu tố kích hoạt: Xác định và tránh thực phẩm, mùi, ánh sáng gây đau đầu
9. Sử dụng tinh dầu bạc hà: Xoa nhẹ lên thái dương có thể giúp giảm đau
10. Thuốc giảm đau không kê đơn: Paracetamol, Ibuprofen, Aspirin (tham khảo ý kiến bác sĩ)

Với đau nửa đầu (migraine): Nằm nghỉ trong phòng tối, chườm lạnh, và uống thuốc khi có dấu hiệu đầu tiên.

Nên đi khám nếu đau đầu dữ dội đột ngột, kèm sốt cao, cứng cổ, buồn nôn, nôn mửa, hoặc thay đổi ý thức.
""",

    "ho": """
Dưới đây là các biện pháp giảm ho hiệu quả:

1. Uống nhiều nước: Giữ đủ nước giúp làm loãng đờm và giảm kích thích
2. Dùng máy tạo độ ẩm: Tăng độ ẩm không khí giúp giảm khô họng
3. Súc họng với nước muối: Hòa 1/4 thìa muối trong nước ấm và súc họng
4. Uống mật ong ấm: Mật ong có tính kháng khuẩn, giảm ho (không dùng cho trẻ dưới 1 tuổi)
5. Uống trà gừng: Gừng có tính chống viêm, giúp giảm ho và đau họng
6. Hít hơi nước: Hít hơi nước ấm giúp làm ẩm đường hô hấp
7. Nâng cao đầu khi ngủ: Giảm chảy dịch mũi xuống họng gây kích thích
8. Tránh chất kích thích: Tránh khói thuốc, hóa chất, không khí ô nhiễm
9. Nghỉ ngơi đầy đủ: Giúp cơ thể phục hồi nhanh chóng
10. Ngậm kẹo ho hoặc viên ngậm thảo dược: Giúp tăng tiết nước bọt làm dịu họng
11. Thuốc ho không kê đơn: Có thể dùng thuốc ho khô hoặc long đờm tùy loại ho

Nên đi khám nếu ho kéo dài trên 3 tuần, ho ra máu, khó thở, sốt cao hoặc đau ngực.
""",

    "đau bụng": """
Các cách giảm đau bụng hiệu quả:

1. Chườm ấm nhẹ vùng bụng: Giúp giãn cơ và tăng lưu thông máu
2. Uống trà thảo mộc: Trà bạc hà, trà hoa cúc, trà gừng có thể làm dịu đau bụng
3. Nghỉ ngơi đầy đủ: Nằm nghỉ tư thế thoải mái, thả lỏng cơ bụng
4. Ăn nhẹ: Tránh thức ăn cay, béo, nhiều dầu mỡ khi đau bụng
5. Tránh đồ uống có gas, caffeine và rượu: Các chất này có thể làm tăng kích ứng
6. Massage nhẹ nhàng: Xoa bóp nhẹ vùng bụng theo chiều kim đồng hồ
7. Uống nước đủ: Giúp phòng táo bón - nguyên nhân phổ biến gây đau bụng
8. Thực hành hít thở sâu: Giúp giảm căng thẳng và đau do co thắt
9. Thuốc giảm đau không kê đơn: Paracetamol (không dùng Aspirin với đau bụng)

Nên đi khám ngay nếu đau bụng dữ dội đột ngột, kèm sốt cao, nôn ra máu, phân đen, hoặc đau kéo dài trên 24 giờ.
""",

    "mất ngủ": """
Dưới đây là các biện pháp khắc phục chứng mất ngủ:

1. Duy trì lịch ngủ đều đặn: Đi ngủ và thức dậy cùng giờ mỗi ngày
2. Tạo môi trường ngủ lý tưởng: Phòng tối, yên tĩnh, nhiệt độ mát (20-22°C)
3. Hạn chế thời gian nằm trên giường: Chỉ sử dụng giường để ngủ, không làm việc hay xem TV
4. Tránh caffeine, rượu và nicotine: Đặc biệt trong 4-6 giờ trước khi ngủ
5. Tránh ăn quá no trước khi ngủ: Ăn tối ít nhất 2-3 giờ trước khi đi ngủ
6. Thực hành thư giãn trước khi ngủ: Tắm nước ấm, đọc sách, nghe nhạc nhẹ
7. Hạn chế ánh sáng xanh: Tránh sử dụng điện thoại, máy tính 1-2 giờ trước khi ngủ
8. Tập thể dục đều đặn: Nhưng tránh tập luyện mạnh trước khi ngủ
9. Quản lý stress: Thực hành thiền, hít thở sâu, ghi nhật ký lo âu
10. Sử dụng kỹ thuật thư giãn cơ: Co và giãn từng nhóm cơ từ chân lên đầu
11. Uống trà thảo mộc: Trà hoa cúc, oải hương, lạc tiên có thể giúp dễ ngủ
12. Tránh ngủ trưa quá dài: Nếu cần, chỉ ngủ trưa 20-30 phút

Nên tham khảo ý kiến bác sĩ nếu mất ngủ kéo dài trên 1 tháng hoặc ảnh hưởng nghiêm trọng đến cuộc sống.
""",
}

TREATMENT_REMEDIES_EN = {
    "back pain": """
Here are 14 effective tips to reduce back pain:

1. Proper rest: Rest for 1-2 days then gradually return to activity, avoid extended bed rest
2. Ice or heat therapy: Apply ice during first 48 hours, then switch to heat
3. Gentle exercise: Walking, swimming, yoga help strengthen back muscles
4. Stretching: Stretching exercises improve flexibility and reduce stiffness
5. Maintain proper posture: Keep back straight when sitting and standing
6. Lift properly: Use your legs, not your back, when lifting heavy objects
7. Use supportive chairs: Back support or ergonomic chairs when working
8. Avoid high heels: Wear flat shoes or those with arch support
9. Lose weight if overweight: Reduces pressure on spine
10. Massage: Gentle massage can help relieve muscle tension
11. Use medicated patches: Topical patches can provide temporary relief
12. Stay hydrated: Keeps spinal discs well hydrated
13. Use appropriate mattress: Not too firm or too soft
14. Over-the-counter pain relievers: Paracetamol, Ibuprofen (consult doctor first)

See a doctor if back pain persists over 6 weeks or is accompanied by warning signs like numbness in limbs or loss of bladder/bowel control.
""",

    "headache": """
Here are effective measures to relieve headaches:

1. Rest in a quiet, dark room: Reduce light and sound stimulation
2. Apply cold or warm compress: Cold pack on forehead for tension headaches, warm for sinus headaches
3. Gentle massage: Gently massage temples, neck and scalp
4. Stay hydrated: Dehydration is a common cause of headaches
5. Limit caffeine and alcohol: Both can trigger headaches or make them worse
6. Get adequate sleep: Maintain regular sleep schedule, aim for 7-8 hours
7. Relax your body: Practice relaxation techniques like deep breathing, meditation
8. Avoid triggers: Identify and avoid foods, smells, lights that cause headaches
9. Use peppermint oil: Gently rub on temples can help reduce pain
10. Over-the-counter pain relievers: Paracetamol, Ibuprofen, Aspirin (consult doctor first)

For migraines: Rest in a dark room, apply cold compresses, and take medication at the first sign.

See a doctor if headache is sudden and severe, accompanied by high fever, stiff neck, nausea, vomiting, or changes in consciousness.
""",

    "cough": """
Here are effective measures to relieve cough:

1. Drink plenty of fluids: Staying hydrated helps thin mucus and reduce irritation
2. Use a humidifier: Increased air moisture helps reduce throat dryness
3. Gargle with salt water: Mix 1/4 teaspoon of salt in warm water and gargle
4. Drink warm honey: Honey has antibacterial properties, reduces cough (not for children under 1)
5. Drink ginger tea: Ginger has anti-inflammatory properties, helps reduce cough and sore throat
6. Steam inhalation: Inhaling warm steam helps moisturize respiratory tract
7. Elevate head while sleeping: Reduces postnasal drip that can trigger coughing
8. Avoid irritants: Stay away from smoke, chemicals, polluted air
9. Get adequate rest: Helps your body recover faster
10. Use cough drops or herbal lozenges: Helps increase saliva production to soothe throat
11. Over-the-counter cough medicine: Choose dry cough or expectorant medication depending on cough type

See a doctor if cough persists over 3 weeks, you're coughing up blood, have difficulty breathing, high fever or chest pain.
""",

    "abdominal pain": """
Effective ways to relieve abdominal pain:

1. Apply gentle heat to the abdomen: Helps relax muscles and increase blood flow
2. Drink herbal tea: Peppermint, chamomile, or ginger tea can soothe abdominal pain
3. Get adequate rest: Lie down in a comfortable position, relax abdominal muscles
4. Eat light meals: Avoid spicy, fatty, greasy foods when experiencing abdominal pain
5. Avoid carbonated drinks, caffeine and alcohol: These can increase irritation
6. Gentle massage: Softly massage abdomen in clockwise direction
7. Stay hydrated: Helps prevent constipation - a common cause of abdominal pain
8. Practice deep breathing: Helps reduce stress and pain from cramping
9. Over-the-counter pain relievers: Paracetamol (avoid Aspirin with abdominal pain)

Seek medical attention immediately if abdominal pain is severe and sudden, accompanied by high fever, vomiting blood, black stools, or lasts over 24 hours.
""",

    "insomnia": """
Here are measures to address insomnia:

1. Maintain a regular sleep schedule: Go to bed and wake up at the same time daily
2. Create an ideal sleep environment: Dark, quiet room, cool temperature (68-72°F)
3. Limit time in bed: Use your bed only for sleep, not for working or watching TV
4. Avoid caffeine, alcohol and nicotine: Especially 4-6 hours before bedtime
5. Avoid eating too much before bedtime: Have dinner at least 2-3 hours before sleep
6. Practice relaxation before bed: Take a warm bath, read a book, listen to soft music
7. Limit blue light exposure: Avoid phones and computers 1-2 hours before bed
8. Exercise regularly: But avoid vigorous exercise close to bedtime
9. Manage stress: Practice meditation, deep breathing, journaling worries
10. Use progressive muscle relaxation: Tense and release muscle groups from feet to head
11. Drink herbal tea: Chamomile, lavender, or passion flower tea may help induce sleep
12. Avoid long daytime naps: If needed, limit naps to 20-30 minutes

Consult a doctor if insomnia persists over a month or significantly impacts your life.
""",
}

# Define question type detection patterns
DIAGNOSIS_QUESTIONS_VI = [
    "bị", "có", "đang", "bệnh gì", "là gì", "bị sao", "nguyên nhân", "vì sao", "tại sao", 
    "triệu chứng", "dấu hiệu", "nguy hiểm không", "nguy hiểm", "nghiêm trọng", "chuẩn đoán"
]

TREATMENT_QUESTIONS_VI = [
    "làm gì", "làm sao", "giảm", "chữa", "điều trị", "khắc phục", "cách", "mẹo", "thuốc", 
    "xử lý", "phương pháp", "giải quyết", "trị", "thuyên giảm", "hết", "đỡ", "đỡ hơn"
]

DIAGNOSIS_QUESTIONS_EN = [
    "have", "having", "what is", "is it", "cause", "why", "reason", "symptom", "sign", 
    "dangerous", "serious", "severe", "diagnosis", "worried", "concerned"
]

TREATMENT_QUESTIONS_EN = [
    "how to", "reduce", "relieve", "treat", "treatment", "cure", "remedy", "medicine", 
    "drug", "help", "method", "deal with", "manage", "overcome", "stop", "ease", "get rid"
]

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
    HEALTH_INFO = HEALTH_INFO_VI if language == 'vi' else HEALTH_INFO_EN
    TREATMENTS = TREATMENT_REMEDIES_VI if language == 'vi' else TREATMENT_REMEDIES_EN
    DIAGNOSIS_QUESTIONS = DIAGNOSIS_QUESTIONS_VI if language == 'vi' else DIAGNOSIS_QUESTIONS_EN
    TREATMENT_QUESTIONS = TREATMENT_QUESTIONS_VI if language == 'vi' else TREATMENT_QUESTIONS_EN
    
    # Identify health condition being discussed
    health_condition = None
    
    # Check for specific health conditions in HEALTH_INFO
    for condition in HEALTH_INFO.keys():
        if condition in message_lower:
            health_condition = condition
            break
    
    # If a health condition was found, determine if this is a treatment question or diagnosis question
    if health_condition:
        # Check if this is a treatment/remedy question
        is_treatment_question = any(term in message_lower for term in TREATMENT_QUESTIONS)
        
        # Check if this is a diagnosis/information question
        is_diagnosis_question = any(term in message_lower for term in DIAGNOSIS_QUESTIONS)
        
        # If it's a treatment question and we have treatment info, provide that
        if is_treatment_question and health_condition in TREATMENTS:
            return TREATMENTS[health_condition]
        
        # If it's a diagnosis question or we couldn't identify question type, provide condition info
        if is_diagnosis_question or not is_treatment_question:
            return HEALTH_INFO[health_condition]
        
        # Default to health info if we can't determine question type
        return HEALTH_INFO[health_condition]
    
    # Check for AI diagnosis keywords
    if any(term in message_lower for term in ["ai diagnosis", "chẩn đoán ai", "chuẩn đoán ai", "ai chẩn đoán", "chẩn đoán"]):
        if language == 'vi':
            return ("Để sử dụng tính năng Chẩn đoán AI, vui lòng chọn các triệu chứng bạn đang gặp phải từ danh sách bên dưới. "
                   "Sau đó, nhấn nút 'Bắt đầu Chẩn đoán' để nhận kết quả phân tích.\n\n"
                   "Đây là công cụ hỗ trợ cung cấp thông tin tham khảo, không thay thế cho chẩn đoán y khoa chuyên nghiệp.")
        else:
            return ("To use the AI Diagnosis feature, please select the symptoms you're experiencing from the list below. "
                   "Then, click the 'Start Diagnosis' button to receive the analysis results.\n\n"
                   "This is a supportive tool providing reference information and does not replace professional medical diagnosis.")
    
    # Check if multiple symptoms are mentioned - suggest AI diagnosis
    from .ai_diagnosis import SYMPTOMS, SYMPTOMS_VI
    
    symptoms_to_check = SYMPTOMS_VI if language == 'vi' else SYMPTOMS
    symptom_translations = dict(zip(SYMPTOMS_VI, SYMPTOMS)) if language == 'vi' else {}
    
    mentioned_symptoms = []
    for symptom in symptoms_to_check:
        symptom_lower = symptom.lower()
        if symptom_lower in message_lower:
            if language == 'vi' and symptom in symptom_translations:
                mentioned_symptoms.append(symptom_translations[symptom])
            else:
                mentioned_symptoms.append(symptom)
    
    # If multiple symptoms mentioned, suggest AI diagnosis
    if len(mentioned_symptoms) >= 2:
        if language == 'vi':
            return (f"Tôi nhận thấy bạn đang mô tả nhiều triệu chứng khác nhau: {', '.join(mentioned_symptoms)}. "
                   f"Bạn có muốn sử dụng tính năng Chẩn đoán AI của chúng tôi không? "
                   f"Nó có thể giúp phân tích các triệu chứng của bạn và đưa ra gợi ý.\n\n"
                   f"Để bắt đầu, hãy gõ 'chẩn đoán AI' hoặc chọn các triệu chứng từ danh sách và nhấn nút 'Bắt đầu Chẩn đoán'.")
        else:
            return (f"I notice you're describing multiple symptoms: {', '.join(mentioned_symptoms)}. "
                   f"Would you like to use our AI Diagnosis feature? "
                   f"It can help analyze your symptoms and provide suggestions.\n\n"
                   f"To begin, type 'AI diagnosis' or select symptoms from the list and click the 'Start Diagnosis' button.")
    
    # Emergency symptom detection - prioritize these responses
    emergency_symptoms_vi = ["đau ngực dữ dội", "khó thở nặng", "đau ngực lan tay trái", "không cử động được", 
                             "mất ý thức", "liệt nửa người", "nói ngọng đột ngột", "méo miệng", "đau đầu dữ dội"]
    emergency_symptoms_en = ["severe chest pain", "severe shortness of breath", "chest pain radiating", "can't move", 
                             "unconscious", "sudden paralysis", "slurred speech", "facial drooping", "severe headache"]
    
    emergency_symptoms = emergency_symptoms_vi if language == 'vi' else emergency_symptoms_en
    
    # Check for emergency conditions first
    for symptom in emergency_symptoms:
        if symptom in message_lower:
            if language == 'vi':
                return "CẢNH BÁO: Các triệu chứng bạn mô tả có thể là DẤU HIỆU CẤP CỨU! Hãy gọi xe cấp cứu (115) hoặc đến phòng cấp cứu gần nhất ngay lập tức. Không tự lái xe đi nếu bạn đang có các triệu chứng này."
            else:
                return "WARNING: The symptoms you're describing may be signs of a MEDICAL EMERGENCY! Please call emergency services (911) or go to the nearest emergency room immediately. Do not drive yourself if you are experiencing these symptoms."
    
    # Continue with regular processing
    # Check for specific health condition information requests
    for condition, info in HEALTH_INFO.items():
        if condition in message_lower:
            # If it's a question about the condition, provide detailed information
            if any(q in message_lower for q in ["what is", "tell me about", "what causes", "symptoms of", "là gì", "triệu chứng", "nguyên nhân", "dấu hiệu", "là sao", "thế nào"]):
                return info
            # If it's also related to doctor recommendation, suggest a specialist after providing info
            if any(term in message_lower for term in ["doctor", "specialist", "bác sĩ", "chuyên gia", "bác sỹ", "khám", "chữa"]):
                specialty = CONDITION_TO_SPECIALTY.get(condition, "Tim mạch")  # Default to cardiology
                doctor_info = get_doctors_by_specialty(specialty, language)
                return f"{info}\n\n---\n\n{doctor_info}"
    
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
