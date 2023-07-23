from django.db.models import TextChoices

from apps.common.utils import get_text_choice_by_value
from meme_wars.tests.test_case import TestCase


class TestGetTextChoiceByValue(TestCase):
    class Choices(TextChoices):
        A = "a", "A"
        B = "b", "B"

    def test_should_return_text_choice_by_value(self):
        text_choice = get_text_choice_by_value(value="a", text_choices=self.Choices)
        self.assertIs(text_choice, self.Choices.A)

    def test_should_raise_value_error_when_choice_does_not_exist(self):
        try:
            get_text_choice_by_value(value="c", text_choices=self.Choices)
        except ValueError as error:
            self.assertEqual(str(error), f'Value "c" is not {self.Choices}')
