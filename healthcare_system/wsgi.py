"""
WSGI config for healthcare_system project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare_system.settings')

application = get_wsgi_application()
