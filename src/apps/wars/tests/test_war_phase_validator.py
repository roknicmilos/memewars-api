from apps.wars.models import War
from apps.wars.tests.factories import WarFactory
from apps.wars.validators import WarPhaseValidator
from meme_wars.tests.test_case import TestCase


class TestWarPhaseValidator(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = WarPhaseValidator(phase_value=War.Phases.SUBMISSION.value)

    def test_should_raise_validation_error_when_war_is_not_in_submission_phase(self):
        expected_message = f'War must be in "{War.Phases.SUBMISSION.label}" phase'
        war = WarFactory()
        self.assertNotEqual(war.phase, War.Phases.SUBMISSION.value)
        with self.raisesDjangoValidationError(match=expected_message):
            self.validator(value=war.pk)
        with self.raisesDjangoValidationError(match=expected_message):
            self.validator(value=war)

    def test_should_not_raise_validation_error_when_war_is_in_submission_phase(self):
        war = WarFactory(phase=War.Phases.SUBMISSION)
        self.validator(value=war.pk)
        self.validator(value=war)
