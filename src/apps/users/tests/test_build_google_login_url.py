from unittest.mock import patch
from urllib.parse import urlencode

from django.conf import settings

from apps.users.authentication import google_openid_config
from apps.users.utils import _create_login_url_query_params, build_google_login_url
from meme_wars.tests.test_case import TestCase
from meme_wars.utils import build_absolute_uri


class TestBuildGoogleLoginURL(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.fetch_google_openid_config_patcher = patch.object(google_openid_config, "_fetch_google_openid_config")
        self.mock_fetch_google_openid_config = self.fetch_google_openid_config_patcher.start()
        self.authorization_endpoint = "https://mock-google-domain/authorization-endpoint/"
        self.mock_fetch_google_openid_config.return_value = {
            "authorization_endpoint": self.authorization_endpoint,
            "token_endpoint": "https://mock-google-domain/token-endpoint/",
        }

    def test_should_create_login_url_query_params(self):
        google_auth_state = "xyz"
        url_query_params = _create_login_url_query_params(state=google_auth_state)
        self.assertEqual(url_query_params["response_type"], "code")
        self.assertEqual(url_query_params["client_id"], settings.GOOGLE_OPENID_CLIENT_ID)
        self.assertEqual(url_query_params["scope"], "openid email profile")
        expected_redirect_uri = build_absolute_uri(view_name="api:users:google_auth:callback")
        self.assertEqual(url_query_params["redirect_uri"], expected_redirect_uri)
        self.assertEqual(url_query_params["state"], google_auth_state)

    @patch("apps.users.utils._create_login_url_query_params")
    def test_should_return_google_login_url(self, mock_create_login_url_query_params):
        url_query_params = {
            "first_param": "first",
            "second_param": "second",
        }
        mock_create_login_url_query_params.return_value = url_query_params
        actual_google_login_url = build_google_login_url(state="xyz")
        expected_google_login_url = f"{self.authorization_endpoint}?{urlencode(url_query_params)}"
        self.assertEqual(actual_google_login_url, expected_google_login_url)
