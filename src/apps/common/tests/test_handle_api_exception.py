from unittest.mock import patch

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated

from apps.common.utils import handle_api_exception
from meme_wars.tests.test_case import TestCase


class TestHandleAPIException(TestCase):
    def test_should_return_response_401_when_auth_token_is_not_provided(self):
        response = handle_api_exception(error=NotAuthenticated())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {"message": "Authentication token was not provided"})

    def test_should_return_response_401_when_auth_token_is_invalid(self):
        response = handle_api_exception(error=AuthenticationFailed())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {"message": "Authentication token is invalid"})

    @patch("apps.common.utils.exception_handler")
    def test_should_call_base_exception_handler_when_it_is_not_auth_token_error(self, mock_base_exception_handler):
        error = Exception()
        handle_api_exception(error=error)
        self.assertEqual(mock_base_exception_handler.call_count, 1)
        self.assertEqual(mock_base_exception_handler.call_args.kwargs, {"exc": error, "context": None})

    def test_should_return_response_400_when_there_is_a_validation_error(self):
        error_message = "Validation error message"

        # When error has a code:
        response = handle_api_exception(error=DjangoValidationError(message=error_message))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"ALL": [error_message]})

        # When error doesn't have a code:
        response = handle_api_exception(error=DjangoValidationError(message=error_message, code="fake_error_code"))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"ALL": [error_message], "code": "fake_error_code"})
