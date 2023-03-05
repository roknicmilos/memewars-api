import uuid

import pytest
import re
import contextlib

from django.core.exceptions import ValidationError
from django.core.handlers.wsgi import WSGIRequest
from django.test import Client
from unittest import TestCase as BaseTestCase


@pytest.mark.django_db
class TestCase(BaseTestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.http_host = 'memewars'
        self.client = Client(HTTP_HOST=self.http_host)

    def get_request_example(self, url_query_params: dict = None) -> WSGIRequest:
        requests = self.client.get(path='/', data=url_query_params).wsgi_request
        if url_query_params:
            requests.query_params = url_query_params
        return requests

    @contextlib.contextmanager
    def raisesValidationError(self, match: str | dict) -> None:
        if isinstance(match, dict):
            match = re.escape(str(match))
        with pytest.raises(expected_exception=ValidationError, match=match):
            yield

    def assertUUIDString(self, value: str) -> None:
        try:
            uuid.UUID(value)
        except ValueError:  # pragma: no cover
            self.fail(f'{value} is not a valid UUID')
