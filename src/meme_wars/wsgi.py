import os
from django.core.wsgi import get_wsgi_application

environment = os.getenv('APP_ENV', 'development').lower()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'meme_wars.settings.{environment}')

application = get_wsgi_application()
