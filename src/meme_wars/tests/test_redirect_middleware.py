import os
from unittest.mock import patch

from django.http import HttpResponseRedirect, HttpResponse
from django.test import override_settings
from django.urls import reverse
from faker import Faker

from apps.common.tests import TestCase


class TestRedirectMiddleware(TestCase):
    faker = Faker()
    mock_api_redirect_url = faker.url()
    mock_admin_redirect_url = faker.url()

    @patch.dict(os.environ, {'API_REDIRECT_URL': ''}, clear=True)
    def test_should_not_redirect_api_request_when_api_redirect_url_is_undefined(self):
        response = self.client.get(path=reverse('api:index'))
        self.assertEqual(response.status_code, 200)

    @override_settings(API_REDIRECT_URL=mock_api_redirect_url)
    def test_should_redirect_api_request_when_api_redirect_url_is_defined(self):
        url_path = reverse('api:index')
        response = self.client.get(path=url_path)
        self.assertRedirects(response=response, expected_url=f'{self.mock_api_redirect_url}{url_path[1:]}')

    @patch.dict(os.environ, {'ADMIN_REDIRECT_URL': ''}, clear=True)
    def test_should_not_redirect_admin_request_when_admin_redirect_url_is_undefined(self):
        self.create_and_login_superuser()
        response = self.client.get(path=reverse('admin:index'))
        self.assertEqual(response.status_code, 200)

    @override_settings(ADMIN_REDIRECT_URL=mock_admin_redirect_url)
    def test_should_redirect_admin_request_when_admin_redirect_url_is_defined(self):
        self.create_and_login_superuser()
        url_path = reverse('admin:index')
        response = self.client.get(path=url_path)
        self.assertRedirects(response=response, expected_url=f'{self.mock_admin_redirect_url}{url_path[1:]}')

    def assertRedirects(self, response: HttpResponse, expected_url: str) -> None:
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.status_code, HttpResponseRedirect.status_code)
        self.assertEqual(response.url, expected_url)
