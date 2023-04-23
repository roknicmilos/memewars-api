from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
import jwt
import requests
from rest_framework import serializers

from apps.common.utils import build_absolute_uri
from apps.users.authentication import GoogleUser, GoogleOpenIDConfig
from apps.users.models import User
from apps.users.utils import get_or_create_user


class GoogleAuthCallbackQuerySerializer(serializers.Serializer):
    state = serializers.CharField(write_only=True)
    email = serializers.CharField()
    given_name = serializers.CharField()
    family_name = serializers.CharField()
    picture = serializers.URLField()

    class Meta:
        model = GoogleUser
        fields = '__all__'

    def __init__(self, request: WSGIRequest = None, **kwargs):
        self.request = request
        super().__init__(**kwargs)

    def is_valid(self, *, raise_exception=False) -> bool:
        if self.request.query_params['state'] != self.request.session['google_auth_state'] and raise_exception:
            raise PermissionError('Invalid Google auth state')
        self.initial_data = self._get_initial_data()
        return super().is_valid(raise_exception=raise_exception)

    def _get_initial_data(self) -> dict:
        token_id = self._get_user_id_token()
        id_token_payload = jwt.decode(token_id, options={'verify_signature': False})
        return {
            'state': self.request.query_params['state'],
            'email': id_token_payload['email'],
            'given_name': id_token_payload['given_name'],
            'family_name': id_token_payload['family_name'],
            'picture': id_token_payload['picture'],
        }

    def _get_user_id_token(self) -> str:
        openid_config = GoogleOpenIDConfig()
        request_data = self._create_token_endpoint_request_data()
        response = requests.post(
            url=openid_config.token_endpoint,
            data=request_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=5
        )
        response_data = response.json()
        return response_data['id_token']

    def _create_token_endpoint_request_data(self) -> dict:
        return {
            'code': self.request.query_params.get('code'),
            'client_id': settings.GOOGLE_OPENID_CLIENT_ID,
            'client_secret': settings.GOOGLE_OPENID_CLIENT_SECRET,
            'redirect_uri': build_absolute_uri('api:users:google_auth:callback'),
            'grant_type': 'authorization_code'
        }

    def get_or_create_user(self) -> tuple[User, bool]:
        google_user = self._get_google_user()
        return get_or_create_user(google_user=google_user)

    def _get_google_user(self) -> GoogleUser:
        self.is_valid(raise_exception=True)
        kwargs = self.validated_data
        kwargs.pop('state')
        return GoogleUser(**kwargs)
