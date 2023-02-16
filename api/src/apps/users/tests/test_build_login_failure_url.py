from django.conf import settings

from apps.common.tests import TestCase
from apps.users.utils import build_login_failure_url


class TestBuildLoginFailureUrl(TestCase):

    def test_should_build_and_return_login_failure_url(self):
        actual_login_failure_url = build_login_failure_url()
        client_app_url = settings.CLIENT_APP['URL']
        client_app_login_failure_route = settings.CLIENT_APP['LOGIN_FAILURE_ROUTE']
        expected_login_failure_url = f'{client_app_url}/{client_app_login_failure_route}'
        self.assertEqual(actual_login_failure_url, expected_login_failure_url)
