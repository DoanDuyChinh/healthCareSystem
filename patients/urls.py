from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('create-profile/', views.create_profile_view, name='create_profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),
    path('medical-record/<int:record_id>/', views.medical_record_detail_view, name='medical_record_detail'),
]
