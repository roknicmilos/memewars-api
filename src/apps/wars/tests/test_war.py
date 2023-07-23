from apps.wars.models import Meme, Vote, War
from apps.wars.tests.factories import MemeFactory, VoteFactory, WarFactory
from meme_wars.tests.test_case import TestCase


class TestWar(TestCase):
    def test_war_should_have_expected_default_values(self):
        war = War.objects.create(name="Meme war")
        self.assertEqual(war.phase, War.Phases.PREPARATION)
        self.assertFalse(war.requires_meme_approval)

    def test_should_return_all_votes_that_belong_to_war(self):
        first_war = WarFactory()
        first_memes = MemeFactory.create_batch(size=3, war=first_war)
        second_war = WarFactory()
        second_memes = MemeFactory.create_batch(size=2, war=second_war)

        # Create one Vote for each Meme:
        for meme in Meme.objects.all():
            VoteFactory(meme=meme)

        self.assertEqual(Vote.objects.count(), 5)
        self.assertEqual(Meme.objects.count(), 5)

        self.assertEqual(first_war.votes.count(), len(first_memes))
        for a, b in zip(first_war.votes, Vote.objects.filter(meme__war=first_war)):
            self.assertEqual(a, b)

        self.assertEqual(second_war.votes.count(), len(second_memes))
        for a, b in zip(second_war.votes, Vote.objects.filter(meme__war=second_war)):
            self.assertEqual(a, b)

    def test_should_return_vote_count(self):
        first_war = WarFactory()
        first_memes = MemeFactory.create_batch(size=5, war=first_war)
        second_war = WarFactory()
        second_memes = MemeFactory.create_batch(size=4, war=second_war)

        # Create 1st voter with 3 for the first War:
        first_voter = VoteFactory(meme=first_memes[0]).user
        VoteFactory(meme=first_memes[1], user=first_voter)
        VoteFactory(meme=first_memes[2], user=first_voter)

        # Create 2nd voter with 2 for the first War:
        second_voter = VoteFactory(meme=first_memes[3]).user
        VoteFactory(meme=first_memes[4], user=second_voter)

        # Create 3rd voter with 2 for the first War:
        third_voter = VoteFactory(meme=first_memes[0]).user
        VoteFactory(meme=first_memes[2], user=third_voter)

        # Create a single voter with 5 for the first War:
        single_voter = VoteFactory(meme=second_memes[0]).user
        VoteFactory(meme=second_memes[1], user=single_voter)
        VoteFactory(meme=second_memes[2], user=single_voter)
        VoteFactory(meme=second_memes[3], user=single_voter)

        self.assertEqual(first_war.votes.count(), 7)
        self.assertEqual(first_war.voter_count, 3)

        self.assertEqual(second_war.votes.count(), 4)
        self.assertEqual(second_war.voter_count, 1)

    def test_should_return_meme_count(self):
        first_war = WarFactory()
        MemeFactory.create_batch(size=2, war=first_war)
        second_war = WarFactory()
        MemeFactory(war=second_war)

        self.assertEqual(first_war.meme_count, 2)
        self.assertEqual(second_war.meme_count, 1)
