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
        # When Bearer token is not provided:
        response = self.client.get(path=url_path)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message': 'Authentication token was not provided'})

        # When Bearer token is invalid:
        response = self.client.get(path=url_path, HTTP_AUTHORIZATION='Bearer XYZ')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message': 'Authentication token is invalid'})

    def assertListResponse(self, response: Response, serializer: ModelSerializer) -> None:
        self.assertEqual(response.status_code, 200)
        expected_results = []
        for item in serializer.data:
            item_dict = dict(item)
            if 'image' in item_dict:
                item_dict['image'] = f'http://{self.http_host}{item_dict["image"]}'
            expected_results.append(item_dict)
        response_data = response.json()
        self.assertEqual(response_data['results'], expected_results)

    def authenticate(self, user) -> None:
        token, _ = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token.key)
