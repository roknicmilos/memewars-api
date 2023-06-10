from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect
from django.urls import reverse


class RedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if api_redirect_url := _get_api_redirect_url(request=request):
            return redirect(to=api_redirect_url)

        if admin_redirect_url := _get_admin_redirect_url(request=request):
            return redirect(to=admin_redirect_url)

        return self.get_response(request)


def _get_api_redirect_url(request: WSGIRequest) -> str | None:
    path = request.get_full_path()
    absolute_uri = request.build_absolute_uri()
    api_url = settings.API_REDIRECT_URL
    if api_url and not absolute_uri.startswith(api_url) and path.startswith(reverse('api:index')):
        return _create_redirect_url(base_url=api_url, url_path=path)


def _get_admin_redirect_url(request: WSGIRequest) -> str | None:
    path = request.get_full_path()
    absolute_uri = request.build_absolute_uri()
    admin_url = settings.ADMIN_REDIRECT_URL
    if admin_url and not absolute_uri.startswith(admin_url) and path.startswith(reverse('admin:index')):
        return _create_redirect_url(base_url=admin_url, url_path=path)


def _create_redirect_url(base_url: str, url_path: str) -> str:
    if base_url.endswith('/'):
        base_url = base_url[:-1]
    if url_path.startswith('/'):
        url_path = url_path[1:]
    return f'{base_url}/{url_path}'
