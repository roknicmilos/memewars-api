from django.contrib import admin
from apps.common.tests import TestCase
from apps.users.models import User
from apps.users.tests.factories import UserFactory
from apps.wars.admin import WarAdmin
from apps.wars.models import War, Vote
from apps.wars.tests.factories import MemeFactory, WarFactory, VoteFactory


class TestWarAdmin(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.war_admin = WarAdmin(model=War, admin_site=admin.site)

    def test_should_return_number_of_memes(self):
        war = WarFactory()
        MemeFactory.create_batch(size=2, war=war)
        self.assertEqual(self.war_admin.meme_count(obj=war), 2)

    def test_should_return_number_of_votes(self):
        war = WarFactory()
        memes = MemeFactory.create_batch(size=2, war=war)

        VoteFactory.create_batch(size=2, meme=memes[0])
        VoteFactory.create_batch(size=3, meme=memes[1])
        VoteFactory.create_batch(size=2)

        self.assertEqual(Vote.objects.count(), 7)
        self.assertEqual(self.war_admin.vote_count(obj=war), 5)

    def test_should_return_number_of_voters(self):
        war = WarFactory()
        memes = MemeFactory.create_batch(size=3, war=war)  # each Meme creates 1 User

        VoteFactory(meme=memes[0], user=memes[-1].user)
        VoteFactory(meme=memes[1], user=UserFactory())

        self.assertEqual(User.objects.count(), 4)
        self.assertEqual(self.war_admin.voter_count(obj=war), 2)