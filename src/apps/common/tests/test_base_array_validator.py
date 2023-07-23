from apps.common.validators import BaseArrayValidator
from meme_wars.tests.test_case import TestCase


class TestBaseArrayValidator(TestCase):
    def test_should_raise_validation_error_when_value_is_not_a_list(self):
        validator = BaseArrayValidator()
        with self.raisesDjangoValidationError(match="This field does not store a list"):
            validator(value="string")
