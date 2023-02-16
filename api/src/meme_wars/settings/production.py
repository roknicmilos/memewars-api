# For now fetch the development settings
from .development import *  # noqa: F403, F401

DEBUG = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}

# ##### SECURITY CONFIGURATION ############################
SESSION_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = ['https://memewars.roknicmilos.com', ]

CLIENT_APP['URL'] = 'https://app.memewars.roknicmilos.com'  # noqa: F405
