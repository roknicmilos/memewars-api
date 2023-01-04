# For now fetch the development settings
from .development import *  # noqa: F403, F401

DEBUG = False

# You will have to determine, which hostnames should be served by Django
ALLOWED_HOSTS = []

# ##### SECURITY CONFIGURATION ############################

SESSION_COOKIE_SECURE = True
