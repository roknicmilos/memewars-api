import os
from unittest.mock import patch

from apps.common.templatetags.env import bool_env, env
from meme_wars.tests.test_case import TestCase


class TestEnvTemplatetags(TestCase):
    @patch.dict(os.environ, {"TEST_VAR": "test-var"}, clear=True)
    def test_return_string_environment_variable_when_it_exists(self):
        self.assertEqual(env("TEST_VAR"), "test-var")

    def test_return_default_string_when_environment_variable_is_missing(self):
        # When default value is not passed:
        self.assertEqual(env("TEST_VAR"), "")

        # When default value is passed:
        self.assertEqual(env("TEST_VAR", default="default-var"), "default-var")

    @patch.dict(os.environ, {"TEST_VAR": "true"}, clear=True)
    def test_return_bool_environment_variable_when_it_exists(self):
        self.assertTrue(bool_env("TEST_VAR"))

    def test_return_default_boolean_when_environment_variable_is_missing(self):
        # When default value is not passed:
        self.assertEqual(bool_env("TEST_VAR"), False)

        # When default value is passed:
        self.assertFalse(bool_env("TEST_VAR", default=False))
        self.assertTrue(bool_env("TEST_VAR", default=True))
