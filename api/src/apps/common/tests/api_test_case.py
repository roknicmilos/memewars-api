import pytest
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

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

    def assertListResponse(
            self,
            response: Response,
            expected_items: list[dict],
            expected_total_pages: int = 1
    ) -> None:
        self.assertEqual(response.status_code, 200)
        response_body = response.json()
        pagination = response_body['pagination']
        self.assertEqual(pagination['total_pages'], expected_total_pages)
        self.assertEqual(pagination['total_items'], len(response_body['items']))
        self.assertEqual(response_body['items'], expected_items)

    def authenticate(self, user) -> None:
        token, _ = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token.key)
