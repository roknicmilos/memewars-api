from apps.common.tests import TestCase
from apps.wars.models import War
from apps.wars.tests.factories import VoteFactory, WarFactory, MemeFactory


class TestVote(TestCase):

    def test_should_raise_validation_error_when_creating_vote_for_war_that_is_not_in_submission_phase(self):
        war = WarFactory()
        self.assertNotEqual(war.phase, War.Phases.SUBMISSION)
        meme = MemeFactory(war=war)
        vote = VoteFactory(meme=meme)
        self.assertValidationError(
            obj=vote,
            expected_message=f'Meme must be in a war that is in "{War.Phases.SUBMISSION}" phase',
            field_name='meme',
            expected_code='limit_meme_war_phase',
        )

    def test_should_return_correct_war(self):
        war = WarFactory(phase=War.Phases.SUBMISSION)
        meme = MemeFactory(war=war)
        vote = VoteFactory(meme=meme)
        self.assertEqual(vote.war, war)
