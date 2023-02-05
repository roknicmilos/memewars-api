from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.response import Response
from apps.common.tests import APITestCase
from apps.users.models import User


class TestLoginAPIView(APITestCase):

    def test_should_return_auth_token_when_credentials_are_valid(self):
        password = 'pass4user'
        user = User.objects.create_user(email='example@example.com', password=password)
        data = {
            'email': user.email,
            'password': password,
        }
        self.assertFalse(Token.objects.exists())

        response = self.client.post(path=reverse('api:auth_token'), json=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Token.objects.count(), 1)
        token = Token.objects.filter(user=user).first()
        self.assertEqual(response.json(), {'token': token.key})

    def test_should_return_validation_errors_when_credentials_are_invalid(self):
        # When email is invalid
        password = 'pass4user'
        user = User.objects.create_user(email='example@example.com', password=password)
        data = {
            'email': f'invalid.{user.email}',
            'password': password,
        }
        self.assertFalse(Token.objects.exists())

        response = self.client.post(path=reverse('api:auth_token'), json=data)
        self.assertInvalidCredentials(response=response)
        self.assertFalse(Token.objects.exists())

        # When password is invalid
        data = {
            'email': user.email,
            'password': f'invalid-{password}',
        }
        response = self.client.post(path=reverse('api:auth_token'), json=data)
        self.assertInvalidCredentials(response=response)
        self.assertFalse(Token.objects.exists())

    def assertInvalidCredentials(self, response: Response) -> None:
        self.assertEqual(response.status_code, 400)
        expected_response_body = {
            'errors': {
                'non_field_errors': ['Invalid credentials', ],
            }
        }
        self.assertEqual(response.json(), expected_response_body)
