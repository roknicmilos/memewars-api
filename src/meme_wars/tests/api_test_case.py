import contextlib

import pytest
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError as APIValidationError
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.settings import api_settings

from apps.common.tests import APIClient
from meme_wars.tests import TestCase


@pytest.mark.django_db
class APITestCase(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = APIClient()

    def assertProtectedGETEndpoint(self, url_path: str) -> None:
        self._assert_protected_endpoint(method="get", url_path=url_path)

    def assertProtectedPOSTEndpoint(self, url_path: str, data: dict) -> None:
        self._assert_protected_endpoint(method="post", url_path=url_path, data=data)

    def assertProtectedDELETEEndpoint(self, url_path: str) -> None:
        self._assert_protected_endpoint(method="delete", url_path=url_path)

    def assertProtectedPATCHEndpoint(self, url_path: str, data: dict) -> None:
        self._assert_protected_endpoint(method="patch", url_path=url_path, data=data)

    def _assert_protected_endpoint(self, method: str, url_path: str, data: dict = None) -> None:
        supported_methods = ["get", "post", "delete", "patch"]
        if method not in supported_methods:
            self.fail(f'Method "{method}" is not supported')
        if method == "post" and data is None:
            self.fail('Method "post" requires data')

        method_func = getattr(self.client, method)
        method_kwargs = {
            "path": url_path,
        }
        if data is not None:
            method_kwargs["data"] = data

        # When Bearer token is not provided:
        response = method_func(**method_kwargs)
        self.assertMissingAuthToken(response=response)

        # When Bearer token is invalid:
        method_kwargs["HTTP_AUTHORIZATION"] = "Bearer XYZ"
        response = method_func(**method_kwargs)
        self.assertInvalidAuthToken(response=response)

    def assertMissingAuthToken(self, response: Response) -> None:
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"message": "Authentication token was not provided"})

    def assertInvalidAuthToken(self, response: Response) -> None:
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"message": "Authentication token is invalid"})

    def assertListResponse(self, response: Response, serializer: ModelSerializer) -> None:
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data["results"]), len(serializer.data))
        self.assertEqual(response_data["results"], serializer.data)

    def authenticate(self, user) -> None:
        token, _ = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token.key)

    @contextlib.contextmanager
    def raisesAPIValidationError(
        self, match: str | dict, code: str = None, field_name: str = api_settings.NON_FIELD_ERRORS_KEY
    ) -> None:
        with pytest.raises(expected_exception=APIValidationError, match=match) as error_info:
            yield

        error_details = error_info.value.get_full_details()
        self.assertIn(field_name, error_details)
        if code:
            field_errors = error_details[field_name]
            if len(field_errors) > 1:
                self.fail(f'There is more than one error for "{field_name}" field.')
            self.assertEqual(field_errors[0]["code"], code)

    def assertBadRequestResponse(self, data: dict, errors: dict[str, list[str]]) -> None:
        response = self.client.post(path=self.url_path, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), errors)
