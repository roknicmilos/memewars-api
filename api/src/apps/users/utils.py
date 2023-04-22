from urllib.parse import urlencode
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework.authtoken.models import Token

from apps.users.authentication import GoogleUser
from apps.users.models import User, UserSettings


def get_or_create_user(google_user: GoogleUser) -> tuple[User, bool]:
    UserSettings.validate_email(email=google_user.email)
    defaults = {
        'first_name': google_user.given_name,
        'last_name': google_user.family_name,
        'image_url': google_user.picture,
    }
    user, is_created = User.objects.get_or_create(email=google_user.email, defaults=defaults)
    if not is_created:
        user.update(**defaults)
    return user, is_created


def build_login_success_url(token: Token) -> str:
    url_query_params = {
        'has_authenticated_successfully': True,
        'token': token.key,
        'email': token.user.email,
        'first_name': token.user.first_name,
        'last_name': token.user.last_name,
        'image_url': token.user.image_url,
    }
    return f'{settings.CLIENT_APP_URL}?{urlencode(url_query_params)}'


def build_login_failure_url(error: Exception = None) -> str:
    url_query_params = {
        'has_authenticated_successfully': False,
        'code': error.code if isinstance(error, ValidationError) else 'unknown_error',
    }
    return f'{settings.CLIENT_APP_URL}?{urlencode(url_query_params)}'
