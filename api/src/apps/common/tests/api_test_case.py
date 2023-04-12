import pytest
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from apps.common.tests import APIClient, TestCase


@pytest.mark.django_db
class APITestCase(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = APIClient(HTTP_HOST=self.http_host)

    def assertProtectedGETEndpoint(self, url_path: str) -> None:
        self._assert_protected_endpoint(method='get', url_path=url_path)

    def assertProtectedPOSTEndpoint(self, url_path: str, data: dict) -> None:
        self._assert_protected_endpoint(method='post', url_path=url_path, data=data)

    def assertProtectedDELETEEndpoint(self, url_path: str) -> None:
        self._assert_protected_endpoint(method='delete', url_path=url_path)

    def _assert_protected_endpoint(self, method: str, url_path: str, data: dict = None) -> None:
        supported_methods = ['get', 'post', 'delete']
        if method not in supported_methods:
            self.fail(f'Method "{method}" is not supported')
        if method == 'post' and data is None:
            self.fail('Method "post" requires data')

        method_func = getattr(self.client, method)
        method_kwargs = {
            'path': url_path,
        }
        if data is not None:
            method_kwargs['data'] = data

        # When Bearer token is not provided:
        response = method_func(**method_kwargs)
        self.assertMissingAuthToken(response=response)

        # When Bearer token is invalid:
        method_kwargs['HTTP_AUTHORIZATION'] = 'Bearer XYZ'
        response = method_func(**method_kwargs)
        self.assertInvalidAuthToken(response=response)

    def assertMissingAuthToken(self, response: Response) -> None:
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message': 'Authentication token was not provided'})

    def assertInvalidAuthToken(self, response: Response) -> None:
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message': 'Authentication token is invalid'})

    def assertListResponse(self, response: Response, serializer: ModelSerializer) -> None:
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data['results']), len(serializer.data))
        self.assertEqual(response_data['results'], serializer.data)

    def authenticate(self, user) -> None:
        token, _ = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token.key)
