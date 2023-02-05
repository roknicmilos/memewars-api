from os import getenv

from django.core.handlers.wsgi import WSGIRequest


def meme_wars(request: WSGIRequest) -> dict:
    return {
        'environment': getenv('ENVIRONMENT'),
        'app_url': getenv('APP_URL'),
    }
