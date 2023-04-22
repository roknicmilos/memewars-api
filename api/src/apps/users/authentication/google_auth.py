import os
import hashlib
from urllib.parse import urlencode
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest

from apps.common.utils import build_absolute_uri
from apps.users.authentication import GoogleOpenIDConfig


def get_login_url(request: WSGIRequest) -> str:
    openid_config = GoogleOpenIDConfig()
    url_query_params = _create_login_url_query_params(request=request)
    return f'{openid_config.authorization_endpoint}?{urlencode(url_query_params)}'


def _create_login_url_query_params(request: WSGIRequest) -> dict:
    request.session['google_auth_state'] = _generate_google_auth_state()
    return {
        'response_type': 'code',
        'client_id': settings.GOOGLE_OPENID_CLIENT_ID,
        'scope': 'openid email profile',
        'redirect_uri': build_absolute_uri('api:users:google_auth:callback'),
        'state': request.session['google_auth_state'],
    }


def _generate_google_auth_state() -> str:
    return hashlib.sha256(os.urandom(1024)).hexdigest()
