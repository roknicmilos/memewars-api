from unittest.mock import patch

from rest_framework.exceptions import NotAuthenticated, AuthenticationFailed

from apps.common.tests import TestCase
from apps.common.utils import handle_api_exception


class TestHandleAPIException(TestCase):

    def test_should_return_response_401_when_auth_token_is_not_provided(self):
        response = handle_api_exception(error=NotAuthenticated())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {'message': 'Authentication token was not provided'})

    def test_should_return_response_401_when_auth_token_is_invalid(self):
        response = handle_api_exception(error=AuthenticationFailed())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {'message': 'Authentication token is invalid'})

    @patch('apps.common.utils.exception_handler')
    def test_should_call_base_exception_handler_when_it_is_not_auth_token_error(self, mock_base_exception_handler):
        error = Exception()
        handle_api_exception(error=error)
        self.assertEqual(mock_base_exception_handler.call_count, 1)
        self.assertEqual(mock_base_exception_handler.call_args.kwargs, {'exc': error, 'context': None})
