from django.core.handlers.wsgi import WSGIRequest
from rest_framework import serializers

from apps.users.models import LoginInProgress
from apps.users.utils import build_google_login_url


class GoogleAuthLoginQuerySerializer(serializers.Serializer):
    login_success_redirect_url = serializers.URLField()
    login_failure_redirect_url = serializers.URLField()

    def __init__(self, request: WSGIRequest = None, **kwargs):
        self.request = request
        super().__init__(**kwargs)

    def is_valid(self, *, raise_exception=False) -> bool:
        self.initial_data = {
            "login_success_redirect_url": self.request.GET.get("login_success_redirect_url"),
            "login_failure_redirect_url": self.request.GET.get("login_failure_redirect_url"),
        }
        if is_valid := super().is_valid(raise_exception=raise_exception):
            LoginInProgress.add_to_session(
                request=self.request,
                login_success_redirect_url=self.validated_data["login_success_redirect_url"],
                login_failure_redirect_url=self.validated_data["login_failure_redirect_url"],
            )

        return is_valid

    @property
    def login_url(self) -> str:
        login_in_progress = LoginInProgress(request=self.request)
        return build_google_login_url(state=login_in_progress.google_auth_state)
