from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest

from meme_wars.urls import API_URL_CONF, ADMIN_URL_CONF, MAIN_URL_CONF


class URLConfMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: WSGIRequest):
        absolute_uri = request.build_absolute_uri()
        if absolute_uri.startswith(settings.API_URL):
            request.urlconf = API_URL_CONF
        elif absolute_uri.startswith(settings.ADMIN_URL):
            request.urlconf = ADMIN_URL_CONF
        else:
            request.urlconf = MAIN_URL_CONF
        return self.get_response(request)
