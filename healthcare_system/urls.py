from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home_view

urlpatterns = [
    # Add the home page URL at the top
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('patients/', include('patients.urls')),
    path('doctors/', include('doctors.urls')),
    path('appointments/', include('appointments.urls')),
    path('pharmacy/', include('pharmacy.urls')),
    path('lab/', include('lab.urls')),
    path('billing/', include('billing.urls')),
    path('adminpanel/', include('adminpanel.urls')),
    path('chat/', include('chatbot.urls')),  # Add chatbot URLs
    # Use a different view for the root URL to avoid namespace conflicts
    path('', include('authentication.urls', namespace='home_auth')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
