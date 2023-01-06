from django.core.exceptions import ValidationError

from apps.common.tests import TestCase
from apps.wars.models import War
from apps.wars.tests.factories import VoteFactory, WarFactory, MemeFactory


class TestVote(TestCase):

    def test_should_raise_validation_error_when_creating_vote_for_war_that_is_not_in_submission_phase(self):
        war = WarFactory()
        self.assertNotEqual(war.phase, War.Phases.SUBMISSION)
        meme = MemeFactory(war=war)
        vote = VoteFactory(meme=meme)
        try:  # TODO: REFACTOR TO ASSERTION FUNCTION ???
            vote.full_clean()
        except ValidationError as error:
            war_field_validation_error = error.error_dict.get('meme')[0]
            expected_error_message = f'Meme must be in a war that is in "{War.Phases.SUBMISSION}" phase'
            self.assertEqual(war_field_validation_error.message, expected_error_message)
            self.assertEqual(war_field_validation_error.code, 'limit_meme_war_phase')
        else:
            self.fail('Did not raise ValidationError')
