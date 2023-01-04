# For now fetch the development settings
from .development import *  # noqa: F403, F401

DEBUG = False

# You will have to determine, which hostnames should be served by Django
ALLOWED_HOST = 'memewars.roknicmilos.com'
ALLOWED_HOSTS = [ALLOWED_HOST]

# ##### SECURITY CONFIGURATION ############################
SESSION_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = [f'https://{ALLOWED_HOST}']
