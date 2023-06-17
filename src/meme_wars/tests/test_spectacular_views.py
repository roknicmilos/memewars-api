from django.conf import settings
from pytest_django.asserts import assertTemplateUsed

from meme_wars.tests import APITestCase
from meme_wars.utils import reverse_api


class TestSpectacularViews(APITestCase):

    def test_should_return_swagger_ui(self):
        response = self.api_client.get(path=reverse_api('schema:swagger'))
        self.assertEqual(response.status_code, 200)
        assertTemplateUsed(response, 'drf_spectacular/swagger_ui.html')

    def test_should_return_redoc_ui(self):
        response = self.api_client.get(path=reverse_api('schema:redoc'))
        self.assertEqual(response.status_code, 200)
        assertTemplateUsed(response, 'drf_spectacular/redoc.html')

    def test_should_download_api_schema(self):
        response = self.api_client.get(path=reverse_api('schema:download'))
        self.assertEqual(response.status_code, 200)
        self.assertEquals(
            response.get('Content-Disposition'),
            f'inline; filename="{settings.SPECTACULAR_SETTINGS["TITLE"]}.yaml"'
        )
