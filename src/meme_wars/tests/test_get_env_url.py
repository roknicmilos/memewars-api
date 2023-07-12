import os
from unittest.mock import patch

import pytest
from decouple import UndefinedValueError
from django.core.exceptions import ValidationError

from meme_wars.tests.test_case import TestCase
from meme_wars.utils import get_env_url


class TestGetEnvURL(TestCase):
    @patch.dict(os.environ, {"TEST_URL": "just.domain.com"}, clear=True)
    def test_should_raise_validation_error_when_url_is_invalid(self):
        invalid_url = os.getenv("TEST_URL")
        expected_error_message = f'[\'Environment variable "TEST_URL" is an invalid URL ("{invalid_url}")\']'
        with pytest.raises(ValidationError, match=expected_error_message):
            get_env_url("TEST_URL")

    def test_should_raise_undefined_value_error_when_url_is_missing_and_default_value_is_not_provided(self):
        missing_url = os.getenv("TEST_URL", default=None)
        self.assertIsNone(missing_url)
        expected_error_message = "TEST_URL not found. Declare it as envvar or define a default value."
        with pytest.raises(UndefinedValueError, match=expected_error_message):
            get_env_url("TEST_URL")

    def test_should_raise_validation_error_when_url_is_missing_and_invalid_default_url_is_provided(self):
        missing_url = os.getenv("TEST_URL", default=None)
        self.assertIsNone(missing_url)
        expected_error_message = '[\'Environment variable "TEST_URL" is an invalid URL ("None")\']'
        with pytest.raises(ValidationError, match=expected_error_message):
            get_env_url("TEST_URL", default=None)

    def test_should_not_raise_validation_error_when_url_is_missing_but_valid_default_url_is_provided(self):
        missing_url = os.getenv("TEST_URL", default=None)
        self.assertIsNone(missing_url)
        get_env_url("TEST_URL", default="https://valid.url.com/")

    def test_should_not_raise_validation_error_when_url_is_valid(self):
        valid_urls = [
            "http://domain.com",
            "http://domain.com/",
            "https://domain.com",
            "https://domain.com/",
        ]
        for url in valid_urls:
            with patch.dict(os.environ, {"TEST_URL": url}, clear=True):
                get_env_url(env_var="TEST_URL")
