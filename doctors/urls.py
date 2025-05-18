from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    path('create-profile/', views.create_profile_view, name='create_profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),
    path('patients/', views.patient_list_view, name='patient_list'),
    path('patients/<int:patient_id>/', views.patient_detail_view, name='patient_detail'),
    path('patients/<int:patient_id>/create-record/', views.create_medical_record_view, name='create_record'),
    path('records/<int:record_id>/', views.record_detail_view, name='record_detail'),
    path('records/<int:record_id>/add-prescription/', views.add_prescription_view, name='add_prescription'),
]
