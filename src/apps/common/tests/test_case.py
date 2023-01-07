from django.core.exceptions import ValidationError
import pytest
from django.core.handlers.wsgi import WSGIRequest
from django.test import Client
from unittest import TestCase as BaseTestCase

from apps.common.models import BaseModel


@pytest.mark.django_db
class TestCase(BaseTestCase):

    @property
    def request(self) -> WSGIRequest:
        client = Client()
        response = client.get('/')
        return response.wsgi_request

    def assertValidationError(
            self,
            obj: BaseModel,
            expected_message: str,
            expected_code: str = None,
            field_name: str = None
    ) -> None:
        try:
            obj.full_clean()
        except ValidationError as error:
            if field_name:
                error = error.error_dict.get(field_name)[0]
            self.assertEqual(error.message, expected_message)
            self.assertEqual(error.code, expected_code)
        else:
            self.fail('Did not raise ValidationError')
