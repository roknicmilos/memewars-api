from rest_framework.response import Response

from meme_wars.tests import APITestCase
from meme_wars.utils import reverse_api, build_absolute_api_uri


class TestAPIIndexView(APITestCase):

    def test_should_return_response_200_with_message(self):
        response = self.api_client.get(path=reverse_api('index'))
        self.assertIsInstance(response, Response)
        self.assertEqual(response.status_code, 200)
        expected_data = {
            'urls': {
                'download_schema': build_absolute_api_uri("schema:download"),
                'swagger_ui': build_absolute_api_uri("schema:swagger"),
                'redoc_ui': build_absolute_api_uri("schema:redoc"),
            }
        }
        self.assertEqual(response.json(), expected_data)
