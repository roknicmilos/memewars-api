from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse


class RedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.get_full_path()

        if path.startswith(reverse('api:index')) and settings.API_REDIRECT_URL:
            return redirect(to=f'{settings.API_REDIRECT_URL}{path[1:]}')

        if path.startswith(reverse('admin:index')) and settings.ADMIN_REDIRECT_URL:
            return redirect(to=f'{settings.ADMIN_REDIRECT_URL}{path[1:]}')

        return self.get_response(request)
