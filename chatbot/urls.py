from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('chat/', views.chat_view, name='chat'),
    path('chat_ai/', views.chat_ai_view, name='chat_ai'),  # Add this line for the AI diagnostic chat
    path('send_message/', views.send_message, name='send_message'),
    path('bot_message/', views.bot_message, name='bot_message'),
    path('create_conversation/', views.create_conversation, name='create_conversation'),
    path('delete_conversation/<int:conversation_id>/', views.delete_conversation, name='delete_conversation'),
    path('ai_diagnosis/', views.ai_diagnosis, name='ai_diagnosis'),
]
