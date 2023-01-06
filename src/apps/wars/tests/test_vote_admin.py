from django.contrib.admin.sites import site as admin_site
from apps.common.tests import TestCase
from apps.common.utils import get_model_admin_change_details_url
from apps.wars.admin import VoteAdmin
from apps.wars.models import Vote
from apps.wars.tests.factories import VoteFactory


class TestVoteAdmin(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.vote_admin = VoteAdmin(model=Vote, admin_site=admin_site)

    def test_should_return_correct_admin_id_string_when_vote_object_is_passed(self):
        vote = VoteFactory()
        actual_admin_id = self.vote_admin.admin_id(obj=vote)
        self.assertEqual(actual_admin_id, f'Vote {vote.pk}')

    def test_should_return_correct_meme_id_string_when_vote_object_is_passed(self):
        vote = VoteFactory()
        actual_meme_id = self.vote_admin.meme_id(obj=vote)
        meme_admin_url = get_model_admin_change_details_url(obj=vote.meme)
        expected_meme_id = f'<a href="{meme_admin_url}">Meme {vote.meme.pk}</a>'
        self.assertEqual(actual_meme_id, expected_meme_id)
