from apps.common.validators import AsteriskValidator
from meme_wars.tests.test_case import TestCase


class TestAsteriskValidator(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = AsteriskValidator()

    def test_should_raise_validation_error_when_there_are_other_values_next_to_asterisk(self):
        expected_message = "The list can't contain other values if asterisk is present in the list"
        with self.raisesDjangoValidationError(match=expected_message):
            self.validator(value=["a", "*"])

    def test_should_not_raise_validation_error_when_asterisk_is_the_only_value(self):
        self.validator(value=["*"])
