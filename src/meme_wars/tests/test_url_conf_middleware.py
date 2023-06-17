from meme_wars.urls import MAIN_URL_CONF, ADMIN_URL_CONF, API_URL_CONF
from meme_wars.tests import APITestCase


class TestURLConfMiddleware(APITestCase):

    def test_should_set_main_urls_to_request(self):
        request = self.client.get('/').wsgi_request
        self.assertEqual(request.urlconf, MAIN_URL_CONF)

    def test_should_set_admin_urls_to_request(self):
        request = self.admin_client.get('/').wsgi_request
        self.assertEqual(request.urlconf, ADMIN_URL_CONF)

    def test_should_set_api_urls_to_request(self):
        request = self.api_client.get('/').wsgi_request
        self.assertEqual(request.urlconf, API_URL_CONF)
