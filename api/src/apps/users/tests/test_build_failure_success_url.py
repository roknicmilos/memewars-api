from urllib.parse import urlencode

from django.conf import settings
from django.core.exceptions import ValidationError

from apps.common.tests import TestCase
from apps.users.utils import build_login_failure_url


class TestBuildLoginFailureURL(TestCase):

    def test_should_build_login_failure_url_when_no_error_is_passed(self):
        actual_login_failure_url = build_login_failure_url()
        url_query_params = {
            'has_authenticated_successfully': False,
            'code': 'unknown_error',
        }
        expected_login_failure_url = f'{settings.CLIENT_APP_URL}?{urlencode(url_query_params)}'
        self.assertEqual(actual_login_failure_url, expected_login_failure_url)

    def test_should_build_login_failure_url_when_generic_error_code(self):
        actual_login_failure_url = build_login_failure_url(error=Exception())
        url_query_params = {
            'has_authenticated_successfully': False,
            'code': 'unknown_error',
        }
        expected_login_failure_url = f'{settings.CLIENT_APP_URL}?{urlencode(url_query_params)}'
        self.assertEqual(actual_login_failure_url, expected_login_failure_url)

    def test_should_build_login_failure_url_with_validation_error_code(self):
        validation_error = ValidationError('message', code='test_error')
        actual_login_failure_url = build_login_failure_url(error=validation_error)
        url_query_params = {
            'has_authenticated_successfully': False,
            'code': validation_error.code,
        }
        expected_login_failure_url = f'{settings.CLIENT_APP_URL}?{urlencode(url_query_params)}'
        self.assertEqual(actual_login_failure_url, expected_login_failure_url)
