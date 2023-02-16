from django.conf import settings
from django.utils.http import urlencode

from apps.users.authentication import GoogleUser
from apps.users.models import User


def get_or_create_user(google_user: GoogleUser) -> tuple[User, bool]:
    defaults = {
        'first_name': google_user.given_name,
        'last_name': google_user.family_name,
        'image_url': google_user.picture,
    }
    user, is_created = User.objects.get_or_create(email=google_user.email, defaults=defaults)
    if not is_created:
        user.update(**defaults)
    return user, is_created


def build_login_success_url(token_key: str, is_new_user: bool) -> str:
    url_query_params = {
        'token': token_key,
        'is_new_user': str(is_new_user).lower(),
    }
    client_app_url = settings.CLIENT_APP['URL']
    login_success_route = settings.CLIENT_APP['LOGIN_SUCCESS_ROUTE']
    return f'{client_app_url}/{login_success_route}?{urlencode(url_query_params)}'


def build_login_failure_url() -> str:
    client_app_url = settings.CLIENT_APP['URL']
    login_failure_route = settings.CLIENT_APP['LOGIN_FAILURE_ROUTE']
    return f'{client_app_url}/{login_failure_route}'
