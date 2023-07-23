from apps.wars.models import War
from apps.wars.tests.factories import MemeFactory, WarFactory
from apps.wars.validators import MemeWarPhaseValidator
from meme_wars.tests.test_case import TestCase


class TestMemeWarPhaseValidator(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = MemeWarPhaseValidator(phase_value=War.Phases.VOTING.value)

    def test_should_raise_validation_error_when_war_is_not_in_voting_phase(self):
        expected_message = f'Meme must be in a war that is in "{War.Phases.VOTING.label}" phase'
        meme = MemeFactory()
        self.assertNotEqual(meme.war.phase, War.Phases.VOTING.value)
        with self.raisesDjangoValidationError(match=expected_message):
            self.validator(value=meme.pk)
        with self.raisesDjangoValidationError(match=expected_message):
            self.validator(value=meme)

    def test_should_not_raise_validation_error_when_war_is_in_voting_phase(self):
        war = WarFactory(phase=War.Phases.VOTING)
        meme = MemeFactory(war=war)
        self.validator(value=meme.pk)
        self.validator(value=meme)
