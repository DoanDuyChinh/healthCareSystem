import random
import json
import logging
from datetime import datetime

# Set up logging
logger = logging.getLogger(__name__)

# Expanded diseases list with more common conditions
DISEASES = [
    "Flu", "Common Cold", "COVID-19", "Seasonal Allergy", 
    "Bronchitis", "Pneumonia", "Sinusitis", "Gastroenteritis",
    "Migraine", "Food Poisoning", "Strep Throat", "Urinary Tract Infection"
]

# Expanded symptoms list
SYMPTOMS = [
    "Fever", "Cough", "Sneezing", "Fatigue", "Loss of Taste/Smell", "Itchy Eyes",
    "Sore Throat", "Headache", "Body Aches", "Chills", "Runny Nose", "Nasal Congestion", 
    "Shortness of Breath", "Nausea", "Vomiting", "Diarrhea", "Abdominal Pain",
    "Dizziness", "Ear Pain", "Wheezing", "Chest Pain", "Rash", "Joint Pain", "Swollen Glands"
]

# Vietnamese translations
DISEASES_VI = [
    "Cúm", "Cảm lạnh thông thường", "COVID-19", "Dị ứng theo mùa", 
    "Viêm phế quản", "Viêm phổi", "Viêm xoang", "Viêm dạ dày ruột",
    "Đau nửa đầu", "Ngộ độc thực phẩm", "Viêm họng liên cầu", "Nhiễm trùng đường tiết niệu"
]

SYMPTOMS_VI = [
    "Sốt", "Ho", "Hắt hơi", "Mệt mỏi", "Mất vị giác/khứu giác", "Ngứa mắt",
    "Đau họng", "Đau đầu", "Đau nhức cơ thể", "Ớn lạnh", "Chảy nước mũi", "Nghẹt mũi", 
    "Khó thở", "Buồn nôn", "Nôn", "Tiêu chảy", "Đau bụng",
    "Chóng mặt", "Đau tai", "Thở khò khè", "Đau ngực", "Phát ban", "Đau khớp", "Sưng hạch"
]

# Disease-symptom correlations matrix - values represent strength of correlation (0-1)
DISEASE_SYMPTOM_CORRELATIONS = {
    # Flu
    0: {0: 0.8, 1: 0.7, 3: 0.8, 8: 0.7, 9: 0.6, 10: 0.5, 11: 0.5},
    
    # Common Cold
    1: {1: 0.8, 2: 0.7, 3: 0.5, 6: 0.6, 10: 0.8, 11: 0.8},
    
    # COVID-19
    2: {0: 0.7, 1: 0.8, 3: 0.8, 4: 0.9, 6: 0.5, 7: 0.6, 8: 0.6, 12: 0.6},
    
    # Seasonal Allergy
    3: {2: 0.9, 5: 0.9, 10: 0.8, 11: 0.7, 19: 0.4},
    
    # Bronchitis
    4: {1: 0.9, 3: 0.6, 6: 0.5, 12: 0.5, 19: 0.7, 20: 0.4},
    
    # Pneumonia
    5: {0: 0.8, 1: 0.9, 3: 0.8, 9: 0.7, 12: 0.8, 20: 0.7},
    
    # Sinusitis
    6: {7: 0.8, 10: 0.7, 11: 0.9, 18: 0.5},
    
    # Gastroenteritis
    7: {0: 0.5, 3: 0.6, 13: 0.8, 14: 0.7, 15: 0.9, 16: 0.8},
    
    # Migraine
    8: {7: 0.9, 13: 0.6, 17: 0.7},
    
    # Food Poisoning
    9: {13: 0.9, 14: 0.9, 15: 0.8, 16: 0.7},
    
    # Strep Throat
    10: {0: 0.7, 6: 0.9, 7: 0.5, 23: 0.7},
    
    # Urinary Tract Infection
    11: {0: 0.5, 16: 0.6}
}

# Disease severity levels (1-5, with 5 being most severe)
DISEASE_SEVERITY = {
    0: 3,  # Flu
    1: 2,  # Common Cold
    2: 4,  # COVID-19
    3: 2,  # Seasonal Allergy
    4: 3,  # Bronchitis
    5: 5,  # Pneumonia
    6: 2,  # Sinusitis
    7: 3,  # Gastroenteritis
    8: 2,  # Migraine
    9: 3,  # Food Poisoning
    10: 3, # Strep Throat
    11: 3  # Urinary Tract Infection
}

# Enhanced rule-based diagnosis with improved probability calculation
def generate_diagnosis(symptoms_vector, language='en'):
    try:
        # Convert input to list if needed
        if not isinstance(symptoms_vector, list):
            symptoms_vector = list(symptoms_vector)
        
        # Pad or truncate the vector if needed
        vector_length = len(SYMPTOMS)
        if len(symptoms_vector) < vector_length:
            symptoms_vector.extend([0] * (vector_length - len(symptoms_vector)))
        elif len(symptoms_vector) > vector_length:
            symptoms_vector = symptoms_vector[:vector_length]
        
        # Calculate probabilities based on symptom correlations
        probabilities = [0.0] * len(DISEASES)
        
        # Count how many symptoms are selected
        symptom_count = sum(1 for s in symptoms_vector if s > 0)
        
        if symptom_count == 0:
            # If no symptoms, equal probability for all diseases
            return create_equal_probability_result(language)
            
        # Calculate probability scores for each disease
        for disease_idx, symptom_weights in DISEASE_SYMPTOM_CORRELATIONS.items():
            disease_score = 0
            relevant_symptoms = 0
            
            # Sum the weights of present symptoms
            for symptom_idx, weight in symptom_weights.items():
                if symptom_idx < len(symptoms_vector) and symptoms_vector[symptom_idx] > 0:
                    disease_score += weight
                    relevant_symptoms += 1
            
            # Normalize by the number of relevant symptoms for this disease
            if relevant_symptoms > 0:
                # Adjust score based on how many of the disease's typical symptoms are present
                typical_symptoms = len(symptom_weights)
                coverage_ratio = relevant_symptoms / typical_symptoms
                
                # Weighted score combines the absolute score and the coverage
                probabilities[disease_idx] = (disease_score / relevant_symptoms) * (0.5 + 0.5 * coverage_ratio)
        
        # Normalize probabilities
        total = sum(probabilities)
        if total > 0:
            probabilities = [p/total for p in probabilities]
        else:
            # If still no match, create equal probabilities
            return create_equal_probability_result(language)
        
        # Add reasonable uncertainty based on symptom count
        # Less symptoms = more uncertainty
        base_uncertainty = max(0.1, 0.3 - (0.02 * symptom_count))
        uncertainties = [base_uncertainty + random.uniform(-0.05, 0.05) for _ in range(len(DISEASES))]
        
        # Build disease list based on probabilities
        diseases_list = DISEASES if language == 'en' else DISEASES_VI
        diseases = []
        for i, (disease, prob, uncertainty) in enumerate(zip(diseases_list, probabilities, uncertainties)):
            # Only include diseases with non-zero probability
            if prob > 0.01:
                diseases.append({
                    'name': disease,
                    'probability': prob,
                    'uncertainty': uncertainty,
                    'severity': DISEASE_SEVERITY.get(i, 2)
                })
        
        # Sort diseases by probability
        diseases.sort(key=lambda x: x['probability'], reverse=True)
        
        # Only keep top 5 most likely conditions
        diseases = diseases[:5]
        
        # Determine which symptoms were selected
        symptoms_list = SYMPTOMS if language == 'en' else SYMPTOMS_VI
        selected_symptoms = [symptoms_list[i] for i, val in enumerate(symptoms_vector) if val > 0 and i < len(symptoms_list)]
        
        # Get most likely disease
        most_likely_index = probabilities.index(max(probabilities)) if max(probabilities) > 0 else 0
        
        # Generate test and treatment recommendations
        test_recommendation = get_test_recommendation(most_likely_index, language)
        treatment_recommendation = get_treatment_recommendation(most_likely_index, language)
        
        # Determine if emergency warning is needed
        emergency_warning = check_for_emergency(symptoms_vector, language)
        
        # Format results
        results = {
            'diagnosis': diseases_list[most_likely_index],
            'diseases': diseases,
            'symptoms': selected_symptoms,
            'test': test_recommendation,
            'medicine': treatment_recommendation,
            'emergency_warning': emergency_warning,
            'symptom_count': symptom_count
        }
        
        return results
    
    except Exception as e:
        logger.error(f"Error generating diagnosis: {str(e)}")
        # Return fallback results
        return create_equal_probability_result(language)

def create_equal_probability_result(language):
    """Create a result with equal probabilities for all diseases"""
    diseases_list = DISEASES if language == 'en' else DISEASES_VI
    prob_value = 1.0 / len(diseases_list)
    
    return {
        'diagnosis': diseases_list[0],
        'diseases': [{
            'name': disease,
            'probability': prob_value,
            'uncertainty': 0.2,
            'severity': DISEASE_SEVERITY.get(i, 2)
        } for i, disease in enumerate(diseases_list)],
        'symptoms': [],
        'test': get_general_checkup_text(language),
        'medicine': get_general_advice_text(language),
        'emergency_warning': "",
        'symptom_count': 0
    }

def get_test_recommendation(disease_index, language):
    """Get appropriate test recommendation based on the disease"""
    test_map_en = {
        0: "Influenza A/B test, blood work",
        1: "Clinical examination, no specific tests needed",
        2: "PCR test, antibody test",
        3: "Allergy skin test, IgE blood test",
        4: "Chest X-ray, sputum culture",
        5: "Chest X-ray, blood tests, sputum culture",
        6: "Sinus CT scan, nasal endoscopy",
        7: "Stool sample, food intolerance tests",
        8: "Neurological examination, possibly MRI",
        9: "Stool culture, food poisoning panel",
        10: "Throat culture, rapid strep test",
        11: "Urine culture, urinalysis"
    }
    
    test_map_vi = {
        0: "Xét nghiệm cúm A/B, xét nghiệm máu",
        1: "Khám lâm sàng, không cần xét nghiệm đặc biệt",
        2: "Xét nghiệm PCR, xét nghiệm kháng thể",
        3: "Xét nghiệm dị ứng da, xét nghiệm IgE máu",
        4: "Chụp X-quang ngực, nuôi cấy đờm",
        5: "Chụp X-quang ngực, xét nghiệm máu, nuôi cấy đờm",
        6: "Chụp CT xoang, nội soi mũi",
        7: "Mẫu phân, xét nghiệm không dung nạp thực phẩm",
        8: "Khám thần kinh, có thể chụp MRI",
        9: "Nuôi cấy phân, xét nghiệm ngộ độc thực phẩm",
        10: "Nuôi cấy họng, xét nghiệm strep nhanh",
        11: "Nuôi cấy nước tiểu, phân tích nước tiểu"
    }
    
    test_map = test_map_en if language == 'en' else test_map_vi
    default = get_general_checkup_text(language)
    
    return test_map.get(disease_index, default)

def get_treatment_recommendation(disease_index, language):
    """Get appropriate treatment recommendation based on the disease"""
    treatment_map_en = {
        0: "Rest, fluids, antipyretics (fever reducers), possibly antiviral medication if diagnosed early",
        1: "Rest, fluids, over-the-counter cold medicines, saline nasal spray",
        2: "Isolation, rest, fluids, monitor oxygen levels, follow current medical guidelines",
        3: "Antihistamines, nasal steroids, avoiding allergens, possibly immunotherapy",
        4: "Rest, fluids, humidifier use, possibly antibiotics if bacterial",
        5: "Antibiotics, rest, fluids, possibly hospitalization for severe cases",
        6: "Nasal corticosteroids, antibiotics if bacterial, nasal irrigation",
        7: "Fluid replacement, bland diet, probiotics, anti-diarrheal medication if needed",
        8: "Dark quiet room, migraine-specific medication, preventive treatment if recurrent",
        9: "Fluid replacement, rest, avoiding solid foods until improved",
        10: "Antibiotics, rest, fluids, throat lozenges",
        11: "Antibiotics, increased fluid intake, urinary pain relievers"
    }
    
    treatment_map_vi = {
        0: "Nghỉ ngơi, uống nhiều nước, thuốc hạ sốt, có thể dùng thuốc kháng virus nếu được chẩn đoán sớm",
        1: "Nghỉ ngơi, uống nhiều nước, thuốc cảm lạnh không kê đơn, xịt mũi nước muối",
        2: "Cách ly, nghỉ ngơi, uống nhiều nước, theo dõi mức oxy, tuân theo hướng dẫn y tế hiện tại",
        3: "Thuốc kháng histamine, steroid xịt mũi, tránh dị nguyên, có thể điều trị miễn dịch",
        4: "Nghỉ ngơi, uống nhiều nước, sử dụng máy tạo độ ẩm, có thể dùng kháng sinh nếu nhiễm khuẩn",
        5: "Kháng sinh, nghỉ ngơi, uống nhiều nước, có thể nhập viện nếu trường hợp nghiêm trọng",
        6: "Corticosteroid xịt mũi, kháng sinh nếu nhiễm khuẩn, rửa mũi",
        7: "Bù nước, ăn nhẹ, probiotics, thuốc chống tiêu chảy nếu cần",
        8: "Phòng tối yên tĩnh, thuốc đặc trị đau nửa đầu, điều trị dự phòng nếu tái phát",
        9: "Bù nước, nghỉ ngơi, tránh thức ăn đặc cho đến khi cải thiện",
        10: "Kháng sinh, nghỉ ngơi, uống nhiều nước, viên ngậm họng",
        11: "Kháng sinh, uống nhiều nước, thuốc giảm đau đường tiết niệu"
    }
    
    treatment_map = treatment_map_en if language == 'en' else treatment_map_vi
    default = get_general_advice_text(language)
    
    return treatment_map.get(disease_index, default)

def get_general_checkup_text(language):
    """Return text for general checkup recommendation"""
    if language == 'en':
        return "General medical check-up with your primary care physician"
    else:
        return "Khám sức khỏe tổng quát với bác sĩ đa khoa của bạn"

def get_general_advice_text(language):
    """Return text for general medical advice"""
    if language == 'en':
        return "Consult with a healthcare professional for proper diagnosis and treatment"
    else:
        return "Tham khảo ý kiến chuyên gia y tế để được chẩn đoán và điều trị phù hợp"

def check_for_emergency(symptoms_vector, language):
    """Check if symptoms indicate a potential emergency"""
    # Critical symptom indices: severe breathing difficulty (12), severe chest pain (20)
    critical_symptoms = [12, 20]
    
    # Check if any critical symptoms are present
    has_critical = any(symptoms_vector[i] > 0 for i in critical_symptoms if i < len(symptoms_vector))
    
    # Check for concerning symptom combinations
    # High fever (0) + severe breathing difficulty (12)
    fever_breathing = symptoms_vector[0] > 0 and symptoms_vector[12] > 0 if len(symptoms_vector) > 12 else False
    
    if has_critical or fever_breathing:
        if language == 'en':
            return "WARNING: Some of your symptoms may require urgent medical attention. Please consider seeking immediate medical care if you experience severe shortness of breath, chest pain, or high fever with difficulty breathing."
        else:
            return "CẢNH BÁO: Một số triệu chứng của bạn có thể cần được chăm sóc y tế khẩn cấp. Vui lòng xem xét tìm kiếm chăm sóc y tế ngay lập tức nếu bạn gặp khó thở nghiêm trọng, đau ngực, hoặc sốt cao kèm khó thở."
    
    return ""

# Format diagnostic results as text for the chatbot
def format_diagnosis_text(results, language='en'):
    try:
        emergency_warning = results.get('emergency_warning', '')
        symptom_count = results.get('symptom_count', 0)
        
        if language == 'en':
            text = f"📊 AI Diagnosis Results:\n\n"
            
            # Add emergency warning if present
            if emergency_warning:
                text += f"⚠️ {emergency_warning}\n\n"
            
            text += f"Based on the {symptom_count} symptom(s) you provided, the most likely condition is: {results['diagnosis']}\n\n"
            
            text += "Probability breakdown:\n"
            for prob in results['diseases']:
                severity_indicator = "⚠️ " if prob.get('severity', 0) >= 4 else ""
                text += f"• {severity_indicator}{prob['name']}: {prob['probability']:.1%} (±{prob['uncertainty']:.1%})\n"
            
            text += f"\nRecommended tests: {results['test']}\n"
            text += f"Suggested treatment: {results['medicine']}\n\n"
            
            text += "📋 Important notes:\n"
            text += "• This is an AI-assisted analysis based on the symptoms you provided\n"
            text += "• The accuracy depends on the symptoms entered\n"
            text += "• Always consult a healthcare professional for proper diagnosis\n"
            
            if symptom_count < 3:
                text += "\n⚠️ Few symptoms provided. For a more accurate assessment, please provide more details about what you're experiencing."
        else:
            text = f"📊 Kết quả chẩn đoán AI:\n\n"
            
            # Add emergency warning if present
            if emergency_warning:
                text += f"⚠️ {emergency_warning}\n\n"
            
            text += f"Dựa trên {symptom_count} triệu chứng bạn đã cung cấp, tình trạng có khả năng cao nhất là: {results['diagnosis']}\n\n"
            
            text += "Phân tích xác suất:\n"
            for prob in results['diseases']:
                severity_indicator = "⚠️ " if prob.get('severity', 0) >= 4 else ""
                text += f"• {severity_indicator}{prob['name']}: {prob['probability']:.1%} (±{prob['uncertainty']:.1%})\n"
            
            text += f"\nXét nghiệm đề xuất: {results['test']}\n"
            text += f"Điều trị gợi ý: {results['medicine']}\n\n"
            
            text += "📋 Lưu ý quan trọng:\n"
            text += "• Đây là phân tích với sự hỗ trợ của AI dựa trên các triệu chứng bạn cung cấp\n"
            text += "• Độ chính xác phụ thuộc vào các triệu chứng được nhập\n"
            text += "• Luôn tham khảo ý kiến chuyên gia y tế để có chẩn đoán chính xác\n"
            
            if symptom_count < 3:
                text += "\n⚠️ Ít triệu chứng được cung cấp. Để đánh giá chính xác hơn, vui lòng cung cấp thêm thông tin về những gì bạn đang gặp phải."
        
        return text
    except Exception as e:
        logger.error(f"Error formatting diagnosis text: {str(e)}")
        if language == 'en':
            return "An error occurred while generating the diagnosis. Please try again or consult with a healthcare professional."
        else:
            return "Đã xảy ra lỗi khi tạo chẩn đoán. Vui lòng thử lại hoặc tham khảo ý kiến chuyên gia y tế."
