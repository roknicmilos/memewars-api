from django.contrib.admin.sites import site as admin_site

from apps.wars.admin import VoteAdmin
from apps.wars.models import Vote
from apps.wars.tests.factories import VoteFactory
from meme_wars.tests.test_case import TestCase
from meme_wars.utils import get_model_admin_change_details_url


class TestVoteAdmin(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.vote_admin = VoteAdmin(model=Vote, admin_site=admin_site)

    def test_should_return_correct_admin_id_string_when_vote_object_is_passed(self):
        vote = VoteFactory()
        actual_admin_id = self.vote_admin.admin_id(obj=vote)
        self.assertEqual(actual_admin_id, f"Vote {vote.pk}")

    def test_should_return_correct_meme_id_string_when_vote_object_is_passed(self):
        vote = VoteFactory()
        actual_meme_id = self.vote_admin.meme_id(obj=vote)
        meme_admin_url = get_model_admin_change_details_url(obj=vote.meme)
        expected_meme_id = f'<a href="{meme_admin_url}">Meme {vote.meme.pk}</a>'
        self.assertEqual(actual_meme_id, expected_meme_id)

    def test_queryset_should_contain_user_email_deterministic_annotation(self):
        self.create_and_login_superuser()
        votes = VoteFactory.create_batch(size=2)

        queryset = self.vote_admin.get_queryset(request=self.get_request_example())
        annotated_values = [item.user_email_deterministic for item in queryset]

        user_emails = [vote.user.email for vote in votes]
        self.assertEqual(sorted(annotated_values), sorted(user_emails))
