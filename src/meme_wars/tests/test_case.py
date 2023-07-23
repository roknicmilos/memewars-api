import contextlib
import re
import uuid
from unittest import TestCase as BaseTestCase

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.handlers.wsgi import WSGIRequest
from django.test import Client
from rest_framework.serializers import Serializer


@pytest.mark.django_db
class TestCase(BaseTestCase):
    class ValidationErrorMessages:
        REQUIRED_FIELD_ERROR_MSG = "This field may not be null."
        INVALID_URL_ERROR_MSG = "Enter a valid URL."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = Client()

    def get_request_example(self, url_query_params: dict = None) -> WSGIRequest:
        requests = self.client.get(path="/", data=url_query_params).wsgi_request
        if url_query_params:
            requests.query_params = url_query_params
        return requests

    @contextlib.contextmanager
    def raisesDjangoValidationError(self, match: str | dict, code: str = None) -> None:
        if isinstance(match, dict):
            match = re.escape(str(match))
        with pytest.raises(expected_exception=DjangoValidationError, match=match) as error_info:
            yield
        if code:
            self.assertEqual(error_info.value.code, code)

    def assertUUIDString(self, value: str) -> None:
        try:
            uuid.UUID(value)
        except ValueError:  # pragma: no cover
            self.fail(f"{value} is not a valid UUID")

    def create_and_login_superuser(self) -> None:
        credentials = {"email": "superuser@example.com", "password": "password"}
        get_user_model().objects.create_superuser(**credentials)
        if not self.client.login(**credentials):
            self.fail("Failed to login superuser")

    def assertSerializerErrors(self, serializer: Serializer, expected_errors: dict[str, list[str]]) -> None:
        for field_name, expected_error_messages in expected_errors.items():
            if field_name not in serializer.errors:
                self.fail(f'Field "{field_name}" does not have any errors.')

            actual_error_messages = [str(error) for error in serializer.errors[field_name]]
            self.assertEqual(actual_error_messages, expected_error_messages)
