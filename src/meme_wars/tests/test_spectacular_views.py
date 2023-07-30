from django.conf import settings
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from meme_wars.tests import APITestCase


class TestSpectacularViews(APITestCase):
    def test_should_return_swagger_ui(self):
        response = self.client.get(path=reverse("api:schema:swagger"))
        self.assertEqual(response.status_code, 200)
        assertTemplateUsed(response, "drf_spectacular/swagger_ui.html")

    def test_should_return_redoc_ui(self):
        response = self.client.get(path=reverse("api:schema:redoc"))
        self.assertEqual(response.status_code, 200)
        assertTemplateUsed(response, "drf_spectacular/redoc.html")

    def test_should_download_api_schema(self):
        response = self.client.get(path=reverse("api:schema:download"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            first=response.get("Content-Disposition"),
            second=f'inline; filename="{settings.SPECTACULAR_SETTINGS["TITLE"]}.yaml"',
        )
