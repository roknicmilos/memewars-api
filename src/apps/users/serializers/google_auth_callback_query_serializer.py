from urllib.parse import urlencode

import jwt
import requests
from django.conf import settings
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.handlers.wsgi import WSGIRequest
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.fields import empty

from apps.common.exceptions import NonFieldAPIValidationError
from apps.users.authentication import GoogleOpenIDConfig, GoogleUser
from apps.users.models import LoginInProgress, User, UserSettings
from apps.users.utils import get_or_create_user
from meme_wars.utils import build_absolute_uri


class GoogleAuthCallbackQuerySerializer(serializers.Serializer):
    state = serializers.CharField(write_only=True)
    email = serializers.CharField()
    given_name = serializers.CharField()
    family_name = serializers.CharField()
    picture = serializers.URLField()

    def __init__(self, request: WSGIRequest = None, **kwargs):
        self.request = request
        super().__init__(**kwargs)
        self._login_in_progress: LoginInProgress | None = None

    def is_valid(self, *, raise_exception=False) -> bool:
        self.initial_data = None
        return super().is_valid(raise_exception=raise_exception)

    def run_validation(self, data=empty):
        self._set_login_in_progress()
        self._validate_google_auth_state()
        self.initial_data = self._get_initial_data()
        return super().run_validation(data=self.initial_data)

    def _set_login_in_progress(self) -> None:
        try:
            self._login_in_progress = LoginInProgress(request=self.request)
        except Exception as error:
            raise NonFieldAPIValidationError(str(error), code="login_in_progress_error")

    def _validate_google_auth_state(self) -> None:
        if self.request.query_params["state"] != self._login_in_progress.google_auth_state:
            raise NonFieldAPIValidationError(_("Access denied."), code="access_denied")

    def _get_initial_data(self) -> dict:
        token_data = self._get_user_id_token_data()
        try:
            UserSettings.validate_email(email=token_data["email"])
        except DjangoValidationError as error:
            raise NonFieldAPIValidationError(error.message, code=error.code)
        return {
            "state": self.request.query_params["state"],
            "email": token_data["email"],
            "given_name": token_data["given_name"],
            "family_name": token_data["family_name"],
            "picture": token_data["picture"],
        }

    def _get_user_id_token_data(self) -> dict:
        token_id = self._get_user_id_token()
        return jwt.decode(token_id, options={"verify_signature": False})

    def _get_user_id_token(self) -> str:
        openid_config = GoogleOpenIDConfig()
        request_data = self._create_token_endpoint_request_data()
        response = requests.post(
            url=openid_config.token_endpoint,
            data=request_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=5,
        )
        response_data = response.json()
        return response_data["id_token"]

    def _create_token_endpoint_request_data(self) -> dict:
        return {
            "code": self.request.query_params["code"],
            "client_id": settings.GOOGLE_OPENID_CLIENT_ID,
            "client_secret": settings.GOOGLE_OPENID_CLIENT_SECRET,
            "redirect_uri": build_absolute_uri("api:users:google_auth:callback"),
            "grant_type": "authorization_code",
        }

    def get_or_create_user(self) -> tuple[User, bool]:
        google_user = self._get_google_user()
        return get_or_create_user(google_user=google_user)

    def _get_google_user(self) -> GoogleUser:
        kwargs = self.validated_data
        kwargs.pop("state")
        return GoogleUser(**kwargs)

    def build_login_failure_url(self) -> str:
        url_query_params = {
            "code": list(self.errors.values())[0][0].code,
        }
        return f"{self._login_in_progress.login_failure_redirect_url}?{urlencode(url_query_params)}"

    def build_login_success_url(self, token: Token) -> str:
        url_query_params = {
            "token": token.key,
            "id": token.user.pk,
            "email": token.user.email,
            "first_name": token.user.first_name,
            "last_name": token.user.last_name,
            "image_url": token.user.image_url or "",
        }
        return f"{self._login_in_progress.login_success_redirect_url}?{urlencode(url_query_params)}"
