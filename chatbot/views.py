from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
import json

from .models import Conversation, Message
from .utils import generate_bot_response
from .ai_diagnosis import generate_diagnosis, format_diagnosis_text, SYMPTOMS, SYMPTOMS_VI

@login_required
def chat_view(request):
    conversations = Conversation.objects.filter(user=request.user).order_by('-updated_at')
    
    # Get active conversation or create new one
    conversation_id = request.GET.get('conversation_id')
    if conversation_id:
        conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
        messages = conversation.messages.all()
    else:
        # Create new conversation if none exists
        if not conversations.exists():
            conversation = Conversation.objects.create(
                user=request.user,
                title="New Conversation"
            )
            # Add welcome message
            Message.objects.create(
                conversation=conversation,
                sender='bot',
                content="Hello! I'm your healthcare assistant. How can I help you today?"
            )
        else:
            conversation = conversations.first()
        
        messages = conversation.messages.all()
    
    context = {
        'conversations': conversations,
        'current_conversation': conversation,
        'messages': messages,
        'symptoms_en': json.dumps(SYMPTOMS),
        'symptoms_vi': json.dumps(SYMPTOMS_VI),
    }
    
    return render(request, 'chatbot/chat.html', context)

@login_required
@require_POST
def send_message(request):
    data = json.loads(request.body)
    conversation_id = data.get('conversation_id')
    message_content = data.get('message', '').strip()
    is_system = data.get('is_system', False)
    
    if not message_content:
        return JsonResponse({'status': 'error', 'message': 'Message cannot be empty'})
    
    # Get or create conversation
    if conversation_id:
        conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    else:
        conversation = Conversation.objects.create(
            user=request.user,
            title=message_content[:30] + "..." if len(message_content) > 30 else message_content
        )
    
    # Save user message
    user_message = Message.objects.create(
        conversation=conversation,
        sender='user',
        content=message_content
    )
    
    # Generate bot response only if not a system message
    bot_message = None
    if not is_system:
        # Generate bot response
        bot_response = generate_bot_response(message_content, request.user)
        
        # Save bot message
        bot_message = Message.objects.create(
            conversation=conversation,
            sender='bot',
            content=bot_response
        )
    
    # Update conversation timestamp
    conversation.updated_at = timezone.now()
    conversation.save()
    
    response_data = {
        'status': 'success',
        'conversation_id': conversation.id,
        'user_message': {
            'id': user_message.id,
            'content': user_message.content,
            'timestamp': user_message.timestamp.strftime('%H:%M')
        }
    }
    
    if bot_message:
        response_data['bot_message'] = {
            'id': bot_message.id,
            'content': bot_message.content,
            'timestamp': bot_message.timestamp.strftime('%H:%M')
        }
    
    return JsonResponse(response_data)

@login_required
@require_POST
def bot_message(request):
    """Endpoint to add a bot message to the conversation"""
    data = json.loads(request.body)
    conversation_id = data.get('conversation_id')
    message_content = data.get('message', '').strip()
    
    if not message_content or not conversation_id:
        return JsonResponse({'status': 'error', 'message': 'Message and conversation ID are required'})
    
    # Get conversation
    conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    
    # Save bot message
    bot_message = Message.objects.create(
        conversation=conversation,
        sender='bot',
        content=message_content
    )
    
    # Update conversation timestamp
    conversation.updated_at = timezone.now()
    conversation.save()
    
    return JsonResponse({
        'status': 'success',
        'message_id': bot_message.id,
        'timestamp': bot_message.timestamp.strftime('%H:%M')
    })

@login_required
@require_POST
def create_conversation(request):
    conversation = Conversation.objects.create(
        user=request.user,
        title="New Conversation"
    )
    
    # Add welcome message
    Message.objects.create(
        conversation=conversation,
        sender='bot',
        content="Hello! I'm your healthcare assistant. How can I help you today?"
    )
    
    return JsonResponse({
        'status': 'success',
        'conversation_id': conversation.id,
        'title': conversation.title
    })

@login_required
@require_POST
def delete_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    conversation.delete()
    
    return JsonResponse({'status': 'success'})

@login_required
@require_POST
def ai_diagnosis(request):
    """Handle AI diagnosis requests"""
    data = json.loads(request.body)
    conversation_id = data.get('conversation_id')
    symptoms_vector = data.get('symptoms', [])
    language = data.get('language', 'en')
    
    # Validate the conversation
    if not conversation_id:
        return JsonResponse({'status': 'error', 'message': 'Conversation ID is required'})
    
    conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    
    # Generate diagnosis
    diagnosis_result = generate_diagnosis(symptoms_vector, language)
    
    # Format the results as text
    diagnosis_text = format_diagnosis_text(diagnosis_result, language)
    
    # Add the diagnosis as a bot message
    bot_message = Message.objects.create(
        conversation=conversation,
        sender='bot',
        content=diagnosis_text
    )
    
    # Update conversation timestamp
    conversation.updated_at = timezone.now()
    conversation.save()
    
    # Prepare detailed diagnosis data for visualization
    diseases_data = []
    if 'diseases' in diagnosis_result:
        # Sort diseases by probability for better visualization
        sorted_diseases = sorted(diagnosis_result['diseases'], key=lambda x: x['probability'], reverse=True)
        # Take top 5 diseases for the chart
        top_diseases = sorted_diseases[:5]
        diseases_data = top_diseases
    
    # Prepare diagnosis data for the frontend
    diagnosis_data = {
        'diseases': diseases_data,
        'symptoms': diagnosis_result.get('symptoms', []),
        'language': language
    }
    
    return JsonResponse({
        'status': 'success',
        'diagnosis': diagnosis_data,
        'message_id': bot_message.id,
        'message_content': diagnosis_text,
        'timestamp': bot_message.timestamp.strftime('%H:%M')
    })

@login_required
def chat_ai_view(request):
    """View for the AI diagnostic chat interface"""
    conversations = Conversation.objects.filter(user=request.user).order_by('-updated_at')
    
    # Get active conversation or create new one
    conversation_id = request.GET.get('conversation_id')
    if conversation_id:
        conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
        messages = conversation.messages.all()
    else:
        # Create new conversation if none exists
        if not conversations.exists():
            conversation = Conversation.objects.create(
                user=request.user,
                title="New AI Diagnostic Chat"
            )
            # Add welcome message
            Message.objects.create(
                conversation=conversation,
                sender='bot',
                content="Welcome to AI Diagnostic Chat! Select symptoms above or describe your health concerns to me."
            )
        else:
            conversation = conversations.first()
        
        messages = conversation.messages.all()
    
    context = {
        'conversations': conversations,
        'current_conversation': conversation,
        'messages': messages,
        'symptoms_en': json.dumps(SYMPTOMS),
        'symptoms_vi': json.dumps(SYMPTOMS_VI),
    }
    
    return render(request, 'chatbot/chat_ai.html', context)
