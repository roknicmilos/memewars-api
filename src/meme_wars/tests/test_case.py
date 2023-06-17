import uuid
import pytest
import re
import contextlib

from unittest import TestCase as BaseTestCase
from urllib.parse import urlsplit
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.handlers.wsgi import WSGIRequest
from django.test import Client

from rest_framework.serializers import Serializer


@pytest.mark.django_db
class TestCase(BaseTestCase):
    class ValidationErrorMessages:
        REQUIRED_FIELD_ERROR_MSG = 'This field may not be null.'
        INVALID_URL_ERROR_MSG = 'Enter a valid URL.'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        main_url_parts = urlsplit(settings.HOST_URL)
        self.client = Client(HTTP_HOST=f'{main_url_parts.hostname}:{main_url_parts.port}')

        admin_url_parts = urlsplit(settings.ADMIN_URL)
        self.admin_client = Client(HTTP_HOST=f'{admin_url_parts.hostname}:{admin_url_parts.port}')

    def get_request_example(self, url_query_params: dict = None) -> WSGIRequest:
        requests = self.client.get(path='/', data=url_query_params).wsgi_request
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
            self.fail(f'{value} is not a valid UUID')

    def create_and_login_superuser(self) -> None:
        credentials = {'email': 'superuser@example.com', 'password': 'password'}
        get_user_model().objects.create_superuser(**credentials)
        if not self.admin_client.login(**credentials):
            self.fail('Failed to login superuser')

    def assertSerializerErrors(self, serializer: Serializer, expected_errors: dict[str, list[str]]) -> None:
        for field_name, expected_error_messages in expected_errors.items():
            if field_name not in serializer.errors:
                self.fail(f'Field "{field_name}" does not have any errors.')

            actual_error_messages = [str(error) for error in serializer.errors[field_name]]
            self.assertEqual(actual_error_messages, expected_error_messages)
