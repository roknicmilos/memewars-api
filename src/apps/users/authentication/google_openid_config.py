import requests
from django.conf import settings


class GoogleOpenIDConfig:
    def __init__(self):
        config = _fetch_google_openid_config()
        self.authorization_endpoint = config["authorization_endpoint"]
        self.token_endpoint = config["token_endpoint"]


def _fetch_google_openid_config() -> dict:  # pragma: no cover
    response = requests.get(url=settings.GOOGLE_OPENID_CONFIG_URL, timeout=5)
    return response.json()
