from django.urls import reverse

from meme_wars.tests import APITestCase
from meme_wars.utils import build_absolute_uri


class TestAPIIndexView(APITestCase):
    def test_should_return_response_200_with_message(self):
        response = self.client.get(path=reverse("api:index"))
        self.assertEqual(response.status_code, 200)
        expected_data = {
            "urls": {
                "download_schema": build_absolute_uri("api:schema:download"),
                "swagger_ui": build_absolute_uri("api:schema:swagger"),
                "redoc_ui": build_absolute_uri("api:schema:redoc"),
            }
        }
        self.assertEqual(response.json(), expected_data)
