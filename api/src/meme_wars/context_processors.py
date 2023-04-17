from decouple import config

from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest


def meme_wars(request: WSGIRequest) -> dict:
    return {
        'environment': config('ENVIRONMENT'),
        'app_url': settings.CLIENT_APP_URL,
    }
