from django.conf import settings

from apps.common.tests import TestCase
from apps.users.utils import build_login_success_url


class TestBuildLoginSuccessUrl(TestCase):

    def test_should_build_and_return_login_success_url(self):
        actual_login_success_url = build_login_success_url(token_key='abc', is_new_user=False)
        client_app_url = settings.CLIENT_APP['URL']
        client_app_login_success_route = settings.CLIENT_APP['LOGIN_SUCCESS_ROUTE']
        expected_login_success_url = f'{client_app_url}/{client_app_login_success_route}?token=abc&is_new_user=false'
        self.assertEqual(actual_login_success_url, expected_login_success_url)
