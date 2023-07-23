from urllib.parse import urlencode

from django.conf import settings

from apps.users.authentication import GoogleOpenIDConfig, GoogleUser
from apps.users.models import User
from meme_wars.utils import build_absolute_uri


def get_or_create_user(google_user: GoogleUser) -> tuple[User, bool]:
    defaults = {
        "first_name": google_user.given_name,
        "last_name": google_user.family_name,
        "image_url": google_user.picture,
    }
    user, is_created = User.objects.get_or_create(email=google_user.email, defaults=defaults)
    if not is_created:
        user.update(**defaults)
    return user, is_created


def build_google_login_url(state: str) -> str:
    openid_config = GoogleOpenIDConfig()
    url_query_params = _create_login_url_query_params(state=state)
    return f"{openid_config.authorization_endpoint}?{urlencode(url_query_params)}"


def _create_login_url_query_params(state: str) -> dict:
    return {
        "response_type": "code",
        "client_id": settings.GOOGLE_OPENID_CLIENT_ID,
        "scope": "openid email profile",
        "redirect_uri": build_absolute_uri("api:users:google_auth:callback"),
        "state": state,
    }
