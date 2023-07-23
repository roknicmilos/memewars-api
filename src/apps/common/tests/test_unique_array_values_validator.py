from apps.common.validators import UniqueArrayValuesValidator
from meme_wars.tests.test_case import TestCase


class TestUniqueArrayValuesValidator(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = UniqueArrayValuesValidator()

    def test_should_raise_validation_error_when_list_contains_duplicate_values(self):
        with self.raisesDjangoValidationError(match="The list contains duplicate values"):
            self.validator(value=["a", "b", "a"])

    def test_should_not_raise_validation_error_when_list_contains_unique_values(self):
        self.validator(value=["a", "b", "c"])
