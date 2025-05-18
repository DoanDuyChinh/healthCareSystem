from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('send-message/', views.send_message, name='send_message'),
    path('create-conversation/', views.create_conversation, name='create_conversation'),
    path('delete-conversation/<int:conversation_id>/', views.delete_conversation, name='delete_conversation'),
]
