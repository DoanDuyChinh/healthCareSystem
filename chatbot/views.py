from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
import json

from .models import Conversation, Message
from .utils import generate_bot_response

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
    }
    
    return render(request, 'chatbot/chat.html', context)

@login_required
@require_POST
def send_message(request):
    data = json.loads(request.body)
    conversation_id = data.get('conversation_id')
    message_content = data.get('message', '').strip()
    
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
    
    return JsonResponse({
        'status': 'success',
        'conversation_id': conversation.id,
        'user_message': {
            'id': user_message.id,
            'content': user_message.content,
            'timestamp': user_message.timestamp.strftime('%H:%M')
        },
        'bot_message': {
            'id': bot_message.id,
            'content': bot_message.content,
            'timestamp': bot_message.timestamp.strftime('%H:%M')
        }
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
