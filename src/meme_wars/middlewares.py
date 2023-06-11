from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest


class URLConfMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: WSGIRequest):
        absolute_uri = request.build_absolute_uri()
        if absolute_uri.startswith(settings.API_URL):
            request.urlconf = 'meme_wars.api_urls'
        elif absolute_uri.startswith(settings.ADMIN_URL):
            request.urlconf = 'meme_wars.admin_urls'
        else:
            request.urlconf = 'meme_wars.urls'
        return self.get_response(request)
