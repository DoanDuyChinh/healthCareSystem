"""
ASGI config for healthcare_system project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare_system.settings')

application = get_asgi_application()
