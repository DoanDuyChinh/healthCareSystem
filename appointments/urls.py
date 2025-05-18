from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('book/', views.book_appointment_view, name='book'),
    path('my-appointments/', views.my_appointments_view, name='my_appointments'),
    path('cancel/<int:appointment_id>/', views.cancel_appointment_view, name='cancel'),
    path('doctor-appointments/', views.doctor_appointments_view, name='doctor_appointments'),
    path('update-status/<int:appointment_id>/', views.update_appointment_status_view, name='update_status'),
]
