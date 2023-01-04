from django.core.exceptions import ValidationError
from apps.common.tests import TestCase
from apps.users.tests.factories import UserFactory
from apps.wars.models import Meme, War
from apps.wars.tests.factories import WarFactory


class TestMeme(TestCase):

    def test_should_raise_validation_error_when_war_is_not_in_submission_phase(self):
        user = UserFactory()
        war = WarFactory()
        self.assertNotEqual(war.phase, War.Phases.SUBMISSION)
        meme = Meme(war=war, user=user)
        try:
            meme.full_clean()
        except ValidationError as error:
            war_field_validation_error = error.error_dict.get('war')[0]
            expected_error_message = (
                f'War must be in "{War.Phases.SUBMISSION.label}" phase in order to add a meme to it'
            )
            self.assertEqual(war_field_validation_error.message, expected_error_message)
            self.assertEqual(war_field_validation_error.code, 'limit_war_phase')
