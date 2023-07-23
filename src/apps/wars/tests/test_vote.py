import pytest
from django.db import IntegrityError

from apps.wars.models import War
from apps.wars.tests.factories import MemeFactory, VoteFactory, WarFactory
from meme_wars.tests.test_case import TestCase


class TestVote(TestCase):
    def test_should_raise_integrity_error_when_creating_vote_with_duplicate_meme_and_user_combination(self):
        first_vote = VoteFactory()
        with pytest.raises(IntegrityError) as error_info:
            VoteFactory(user=first_vote.user, meme=first_vote.meme)
        self.assertIn("unique_user_meme", str(error_info.value))

    def test_should_raise_validation_error_when_creating_vote_for_war_that_is_not_in_submission_phase(self):
        war = WarFactory()
        self.assertNotEqual(war.phase, War.Phases.VOTING)
        meme = MemeFactory(war=war)
        vote = VoteFactory(meme=meme)
        expected_validation_errors = {
            "meme": [f'Meme must be in a war that is in "{War.Phases.VOTING.label}" phase'],
        }
        with self.raisesDjangoValidationError(match=expected_validation_errors):
            vote.full_clean()

    def test_should_return_correct_war(self):
        war = WarFactory(phase=War.Phases.VOTING)
        meme = MemeFactory(war=war)
        vote = VoteFactory(meme=meme)
        self.assertEqual(vote.war, war)
