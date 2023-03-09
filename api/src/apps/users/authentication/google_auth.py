import jwt
import os
import hashlib
import requests
from urllib.parse import urlencode
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest

from apps.common.utils import build_absolute_uri
from apps.users.authentication import GoogleOpenIDConfig, GoogleUser


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


def get_user(request: WSGIRequest) -> GoogleUser:
    if request.query_params.get('state') != request.session['google_auth_state']:
        raise PermissionError('Invalid Google auth state')

    token_id = _get_user_id_token(request=request)
    id_token_payload = jwt.decode(token_id, options={'verify_signature': False})

    return GoogleUser(
        email=id_token_payload['email'],
        given_name=id_token_payload['given_name'],
        family_name=id_token_payload['family_name'],
        picture=id_token_payload['picture'],
    )


def _get_user_id_token(request: WSGIRequest) -> str:
    openid_config = GoogleOpenIDConfig()
    request_data = _create_token_endpoint_request_data(request=request)
    response = requests.post(
        url=openid_config.token_endpoint,
        data=request_data,
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    response_data = response.json()
    return response_data['id_token']


def _create_token_endpoint_request_data(request: WSGIRequest) -> dict:
    return {
        'code': request.query_params.get('code'),
        'client_id': settings.GOOGLE_OPENID_CLIENT_ID,
        'client_secret': settings.GOOGLE_OPENID_CLIENT_SECRET,
        'redirect_uri': build_absolute_uri('api:users:google_auth:callback'),
        'grant_type': 'authorization_code'
    }
