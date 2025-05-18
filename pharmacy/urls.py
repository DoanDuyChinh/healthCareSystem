from django.urls import path
from . import views

app_name = 'pharmacy'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('medicines/', views.medicine_list_view, name='medicine_list'),
    path('medicines/add/', views.add_medicine_view, name='add_medicine'),
    path('medicines/edit/<int:medicine_id>/', views.edit_medicine_view, name='edit_medicine'),
    path('dispense/<int:dispense_id>/', views.dispense_medicine_view, name='dispense_medicine'),
    path('prescription/<int:prescription_id>/', views.prescription_view, name='prescription_view'),
    path('request-medicine/<int:prescription_id>/', views.request_medicine_view, name='request_medicine'),
]
