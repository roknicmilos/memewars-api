# For now fetch the development settings
from .development import *  # noqa: F403, F401

DEBUG = False

# ##### SECURITY CONFIGURATION ############################
SESSION_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = ['https://memewars.roknicmilos.com', ]
