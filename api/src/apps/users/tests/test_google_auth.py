from faker import Faker
import pytest
from unittest.mock import patch
from urllib.parse import urlencode
from django.conf import settings
from apps.common.tests import TestCase
from apps.common.utils import build_absolute_uri
from apps.users.authentication import google_openid_config, google_auth
from apps.users.authentication.google_auth import (
    jwt,
    requests,
    _create_login_url_query_params,
    _generate_google_auth_state,
    _get_user_id_token,
    _create_token_endpoint_request_data,
)
from apps.users.tests.factories import TokenFactory


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
        expected_redirect_uri = build_absolute_uri(view_name='api:google_auth:callback')
        self.assertEqual(url_query_params['redirect_uri'], expected_redirect_uri)
        self.assertEqual(url_query_params['state'], mock_generate_google_auth_state.return_value)

    def test_should_raise_permission_error_when_state_from_url_is_not_equal_to_state_from_session(self):
        request = self.get_request_example(url_query_params={'state': 'xyz'})
        request.session['google_auth_state'] = 'abc'
        with pytest.raises(PermissionError, match='Invalid Google auth state'):
            google_auth.get_user(request=request)

    @patch.object(jwt, 'decode')
    @patch.object(google_auth, '_get_user_id_token')
    def test_should_return_google_user(self, _, mock_decode_jwt):
        faker = Faker()
        id_token_payload = {
            'email': faker.email(),
            'given_name': faker.first_name(),
            'family_name': faker.last_name(),
            'picture': 'https://mock-google-domain/profile-image.jpg',
        }
        mock_decode_jwt.return_value = id_token_payload
        request = self.get_request_example(url_query_params={'state': 'xyz'})
        request.session['google_auth_state'] = 'xyz'
        google_user = google_auth.get_user(request=request)
        self.assertEqual(google_user.email, id_token_payload['email'])
        self.assertEqual(google_user.given_name, id_token_payload['given_name'])
        self.assertEqual(google_user.family_name, id_token_payload['family_name'])
        self.assertEqual(google_user.picture, id_token_payload['picture'])

    @patch.object(google_auth, '_create_token_endpoint_request_data', return_value={})
    @patch.object(requests, 'post')
    def test_should_get_user_id_token(self, mock_requests_post, _):
        class ResponseMock:
            id_token = 'response-mock-id-token'

            def json(self) -> dict:
                return {'id_token': self.id_token}

        mock_requests_post.return_value = ResponseMock()
        id_token = _get_user_id_token(request=self.get_request_example())
        self.assertEqual(id_token, ResponseMock.id_token)

    def test_should_return_token_endpoint_request_data(self):
        url_query_params = {
            'code': 'xyz',
        }
        request = self.get_request_example(url_query_params=url_query_params)
        request_data = _create_token_endpoint_request_data(request=request)
        self.assertEqual(request_data['code'], url_query_params['code'])
        self.assertEqual(request_data['client_id'], settings.GOOGLE_OPENID_CLIENT_ID)
        self.assertEqual(request_data['client_secret'], settings.GOOGLE_OPENID_CLIENT_SECRET)
        expected_redirect_uri = build_absolute_uri(view_name='api:google_auth:callback')
        self.assertEqual(request_data['redirect_uri'], expected_redirect_uri)
        self.assertEqual(request_data['grant_type'], 'authorization_code')

    def test_should_build_and_return_login_success_url(self):
        token = TokenFactory()
        actual_login_success_url = google_auth.build_login_success_url(token=token)
        url_query_params = {
            'has_authenticated_successfully': True,
            'toke': token.key,
            'email': token.user.email,
            'first_name': token.user.first_name,
            'last_name': token.user.last_name,
            'image_url': token.user.image_url,
        }
        expected_login_success_url = f'{settings.CLIENT_APP_URL}?{urlencode(url_query_params)}'
        self.assertEqual(actual_login_success_url, expected_login_success_url)

    def test_should_build_and_return_login_failure_url(self):
        actual_login_failure_url = google_auth.build_login_failure_url()
        url_query_params = {
            'has_authenticated_successfully': False,
        }
        expected_login_failure_url = f'{settings.CLIENT_APP_URL}?{urlencode(url_query_params)}'
        self.assertEqual(actual_login_failure_url, expected_login_failure_url)

    def tearDown(self) -> None:
        super().tearDown()
        self.fetch_google_openid_config_patcher.stop()
