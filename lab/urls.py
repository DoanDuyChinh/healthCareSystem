from django.urls import path
from . import views

app_name = 'lab'

urlpatterns = [
    path('order-test/<int:patient_id>/', views.order_test_view, name='order_test'),
    path('update-test/<int:test_id>/', views.update_test_view, name='update_test'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('test/<int:test_id>/', views.test_detail_view, name='test_detail'),
    path('my-tests/', views.patient_tests_view, name='patient_tests'),
]
