from django.test import override_settings, Client

from apps.common.tests import TestCase


class TestURLConfMiddleware(TestCase):

    def test_should_set_main_urls_to_request(self):
        request = self.client.get('/').wsgi_request
        self.assertEqual(request.urlconf, 'meme_wars.urls')

    def test_should_set_admin_urls_to_request(self):
        admin_host = 'admin.host.com'
        admin_client = Client(HTTP_HOST=admin_host)
        admin_url = f'http://{admin_host}/'
        with override_settings(ADMIN_URL=admin_url):
            request = admin_client.get('/').wsgi_request
        self.assertEqual(request.urlconf, 'meme_wars.admin_urls')

    def test_should_set_api_urls_to_request(self):
        api_host = 'api.host.com'
        api_client = Client(HTTP_HOST=api_host)
        api_url = f'http://{api_host}/'
        with override_settings(API_URL=api_url):
            request = api_client.get('/').wsgi_request
        self.assertEqual(request.urlconf, 'meme_wars.api_urls')
