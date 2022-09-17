import os
from django.core.wsgi import get_wsgi_application

environment = os.getenv('APP_ENV', 'development').lower()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'qwerty.settings.{environment}')

application = get_wsgi_application()
