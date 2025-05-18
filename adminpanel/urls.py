from django.urls import path
from . import views

app_name = 'adminpanel'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('users/', views.user_management_view, name='user_management'),
    path('reports/', views.report_view, name='reports'),
    path('settings/', views.system_settings_view, name='system_settings'),
]
