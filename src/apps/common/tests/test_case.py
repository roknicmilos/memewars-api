import pytest
from django.core.handlers.wsgi import WSGIRequest
from django.test import Client
from unittest import TestCase as BaseTestCase


@pytest.mark.django_db
class TestCase(BaseTestCase):

    @property
    def request(self) -> WSGIRequest:
        client = Client()
        response = client.get('/')
        return response.wsgi_request
