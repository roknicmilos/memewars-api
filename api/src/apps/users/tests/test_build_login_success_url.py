from urllib.parse import urlencode

from django.conf import settings

from apps.common.tests import TestCase
from apps.users.tests.factories import TokenFactory
from apps.users.utils import build_login_success_url


class TestBuildLoginSuccessURL(TestCase):

    def test_should_build_and_return_login_success_url(self):
        token = TokenFactory()
        actual_login_success_url = build_login_success_url(token=token)
        url_query_params = {
            'has_authenticated_successfully': True,
            'token': token.key,
            'email': token.user.email,
            'first_name': token.user.first_name,
            'last_name': token.user.last_name,
            'image_url': token.user.image_url,
        }
        expected_login_success_url = f'{settings.CLIENT_APP_URL}?{urlencode(url_query_params)}'
        self.assertEqual(actual_login_success_url, expected_login_success_url)
