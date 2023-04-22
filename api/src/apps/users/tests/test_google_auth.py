from unittest.mock import patch
from urllib.parse import urlencode
from django.conf import settings
from apps.common.tests import TestCase
from apps.common.utils import build_absolute_uri
from apps.users.authentication import google_openid_config, google_auth
from apps.users.authentication.google_auth import (
    _create_login_url_query_params,
    _generate_google_auth_state,
)


class TestGoogleAuth(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.fetch_google_openid_config_patcher = patch.object(google_openid_config, '_fetch_google_openid_config')
        self.mock_fetch_google_openid_config = self.fetch_google_openid_config_patcher.start()
        self.authorization_endpoint = 'https://mock-google-domain/authorization-endpoint/'
        self.token_endpoint = 'https://mock-google-domain/token-endpoint/'
        self.mock_fetch_google_openid_config.return_value = {
            'authorization_endpoint': self.authorization_endpoint,
            'token_endpoint': self.token_endpoint,
        }

    @patch.object(google_auth, '_create_login_url_query_params')
    def test_should_return_google_login_url(self, mock_create_login_url_query_params):
        url_query_params = {
            'first_param': 'first',
            'second_param': 'second',
        }
        mock_create_login_url_query_params.return_value = url_query_params
        actual_google_login_url = google_auth.get_login_url(request=self.get_request_example())
        expected_google_login_url = f'{self.authorization_endpoint}?{urlencode(url_query_params)}'
        self.assertEqual(actual_google_login_url, expected_google_login_url)

    def test_should_return_random_string_value(self):
        string = _generate_google_auth_state()
        self.assertIsInstance(string, str)

    @patch.object(google_auth, '_generate_google_auth_state')
    def test_should_return_login_url_query_params(self, mock_generate_google_auth_state):
        mock_generate_google_auth_state.return_value = 'xyz'
        request = self.get_request_example()
        url_query_params = _create_login_url_query_params(request=request)
        self.assertEqual(request.session['google_auth_state'], mock_generate_google_auth_state.return_value)
        self.assertEqual(url_query_params['response_type'], 'code')
        self.assertEqual(url_query_params['client_id'], settings.GOOGLE_OPENID_CLIENT_ID)
        self.assertEqual(url_query_params['scope'], 'openid email profile')
        expected_redirect_uri = build_absolute_uri(view_name='api:users:google_auth:callback')
        self.assertEqual(url_query_params['redirect_uri'], expected_redirect_uri)
        self.assertEqual(url_query_params['state'], mock_generate_google_auth_state.return_value)

    def tearDown(self) -> None:
        super().tearDown()
        self.fetch_google_openid_config_patcher.stop()
