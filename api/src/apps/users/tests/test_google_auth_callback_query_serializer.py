from faker import Faker
import pytest
from unittest.mock import patch
from django.conf import settings

from apps.common.tests import TestCase
from apps.common.utils import build_absolute_uri
from apps.users import serializers as user_serializers
from apps.users.models import UserSettings
from apps.users.tests.factories import UserFactory


@pytest.mark.django_db
class TestGoogleAuthCallbackQuerySerializer(TestCase):

    def test_should_raise_permission_error_when_state_from_url_is_not_equal_to_state_from_session(self):
        request = self.get_request_example(url_query_params={'state': 'xyz'})
        request.session['google_auth_state'] = 'abc'
        serializer = user_serializers.GoogleAuthCallbackQuerySerializer(request=request)
        with pytest.raises(PermissionError, match='Invalid Google auth state'):
            serializer.get_or_create_user()

    @patch.object(user_serializers.jwt, 'decode')
    @patch.object(user_serializers.GoogleAuthCallbackQuerySerializer, '_get_user_id_token')
    def test_should_return_google_user(self, _, mock_decode_jwt):
        faker = Faker()
        id_token_payload = {
            'email': faker.email(),
            'given_name': faker.first_name(),
            'family_name': faker.last_name(),
            'picture': faker.image_url(),
        }
        UserSettings.update(allowed_emails=[id_token_payload['email']])
        mock_decode_jwt.return_value = id_token_payload
        request = self.get_request_example(url_query_params={'state': 'xyz'})
        request.session['google_auth_state'] = 'xyz'
        serializer = user_serializers.GoogleAuthCallbackQuerySerializer(request=request)
        google_user = serializer._get_google_user()
        self.assertEqual(google_user.email, id_token_payload['email'])
        self.assertEqual(google_user.given_name, id_token_payload['given_name'])
        self.assertEqual(google_user.family_name, id_token_payload['family_name'])
        self.assertEqual(google_user.picture, id_token_payload['picture'])

    @patch.object(
        user_serializers.GoogleAuthCallbackQuerySerializer,
        '_create_token_endpoint_request_data',
        return_value={}
    )
    @patch.object(user_serializers.requests, 'post')
    def test_should_get_user_id_token(self, mock_requests_post, _):
        class ResponseMock:
            id_token = 'response-mock-id-token'

            def json(self) -> dict:
                return {'id_token': self.id_token}

        mock_requests_post.return_value = ResponseMock()
        request = self.get_request_example()
        serializer = user_serializers.GoogleAuthCallbackQuerySerializer(request=request)
        id_token = serializer._get_user_id_token()
        self.assertEqual(id_token, ResponseMock.id_token)

    def test_should_return_token_endpoint_request_data(self):
        url_query_params = {
            'code': 'xyz',
        }
        request = self.get_request_example(url_query_params=url_query_params)
        serializer = user_serializers.GoogleAuthCallbackQuerySerializer(request=request)
        request_data = serializer._create_token_endpoint_request_data()
        self.assertEqual(request_data['code'], url_query_params['code'])
        self.assertEqual(request_data['client_id'], settings.GOOGLE_OPENID_CLIENT_ID)
        self.assertEqual(request_data['client_secret'], settings.GOOGLE_OPENID_CLIENT_SECRET)
        expected_redirect_uri = build_absolute_uri(view_name='api:users:google_auth:callback')
        self.assertEqual(request_data['redirect_uri'], expected_redirect_uri)
        self.assertEqual(request_data['grant_type'], 'authorization_code')

    @patch.object(user_serializers, 'get_or_create_user')
    @patch.object(user_serializers.GoogleAuthCallbackQuerySerializer, '_get_google_user')
    def test_should_create_user(self, _, mock_get_or_create_user):
        mock_get_or_create_user.return_value = [UserFactory(), True]
        request = self.get_request_example()
        serializer = user_serializers.GoogleAuthCallbackQuerySerializer(request=request)
        user, is_created = serializer.get_or_create_user()
        self.assertTrue(is_created)
        self.assertEqual(user, mock_get_or_create_user.return_value[0])

    @patch.object(user_serializers, 'get_or_create_user')
    @patch.object(user_serializers.GoogleAuthCallbackQuerySerializer, '_get_google_user')
    def test_should_get_user(self, _, mock_get_or_create_user):
        mock_get_or_create_user.return_value = [UserFactory(), False]
        request = self.get_request_example()
        serializer = user_serializers.GoogleAuthCallbackQuerySerializer(request=request)
        user, is_created = serializer.get_or_create_user()
        self.assertFalse(is_created)
        self.assertEqual(user, mock_get_or_create_user.return_value[0])
