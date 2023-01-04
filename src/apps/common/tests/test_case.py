import pytest
from unittest import TestCase as BaseTestCase


@pytest.mark.django_db
class TestCase(BaseTestCase):
    pass
