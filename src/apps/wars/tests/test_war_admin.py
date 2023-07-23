from django.contrib import admin

from apps.users.models import User
from apps.users.tests.factories import UserFactory
from apps.wars.admin import WarAdmin
from apps.wars.models import Vote, War
from apps.wars.tests.factories import MemeFactory, VoteFactory, WarFactory
from meme_wars.tests.test_case import TestCase


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

    def test_should_add_meme_upload_limit_field_in_readonly_fields_when_war_is_not_in_submission_phase(self):
        wars = []
        for phase in War.Phases:
            if phase is War.Phases.SUBMISSION:
                wars.append(None)  # to simulate adding a new war
                continue
            wars.append(WarFactory(phase=phase))

        request = self.get_request_example()
        for war in wars:
            readonly_fields = self.war_admin.get_readonly_fields(request=request, obj=war)
            self.assertIn("meme_upload_limit", readonly_fields)

    def test_should_not_add_meme_upload_limit_field_in_readonly_fields_when_war_is_in_submission_phase(self):
        war = WarFactory(phase=War.Phases.SUBMISSION)
        readonly_fields = self.war_admin.get_readonly_fields(request=self.get_request_example(), obj=war)
        self.assertNotIn("meme_upload_limit", readonly_fields)
