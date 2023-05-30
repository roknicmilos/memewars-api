from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse


class RedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.get_full_path()

        if path.startswith(reverse('api:index')) and settings.API_REDIRECT_URL:
            return redirect(to=_create_redirect_url(base_url=settings.API_REDIRECT_URL, url_path=path))

        if path.startswith(reverse('admin:index')) and settings.ADMIN_REDIRECT_URL:
            return redirect(to=_create_redirect_url(base_url=settings.ADMIN_REDIRECT_URL, url_path=path))

        return self.get_response(request)


def _create_redirect_url(base_url: str, url_path: str) -> str:
    if base_url.endswith('/'):
        base_url = base_url[:-1]
    if url_path.startswith('/'):
        url_path = url_path[1:]
    return f'{base_url}/{url_path}'
