from os import getenv

from django.core.handlers.wsgi import WSGIRequest


def meme_wars(request: WSGIRequest) -> dict:
    return {'app_env': getenv('APP_ENV')}
