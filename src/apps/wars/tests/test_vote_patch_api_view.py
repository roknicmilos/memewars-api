from django.urls import reverse

from apps.users.tests.factories import UserFactory
from apps.wars.tests.factories import MemeFactory, VoteFactory
from meme_wars.tests import APITestCase


class TestVotePatchAPIView(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.user = UserFactory()
        self.vote = VoteFactory(score=5, user=self.user)
        self.url_path = reverse("api:votes:details", args=(self.vote.pk,))

    def test_patch_endpoint_should_return_response_401_when_authentication_headers_are_invalid(self):
        self.assertProtectedPATCHEndpoint(url_path=self.url_path, data={})

    def test_patch_endpoint_should_return_response_404_when_vote_does_not_belong_to_authenticated_user(self):
        self.authenticate(user=self.user)

        vote = VoteFactory()
        url_path = reverse("api:votes:details", args=(vote.pk,))
        response = self.client.patch(path=url_path, data={})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"message": "Not found"})

    def test_patch_endpoint_should_return_response_200_and_only_update_vote_score(self):
        self.authenticate(user=self.user)

        original_meme = self.vote.meme
        different_user = UserFactory()
        different_meme = MemeFactory()
        new_score = 6
        data = {
            "user": different_user.pk,
            "meme": different_meme.pk,
            "score": new_score,
            "submission_count": self.vote.submission_count + 5,
        }
        expected_new_submission_count = self.vote.submission_count + 1

        response = self.client.patch(path=self.url_path, data=data)
        self.assertEqual(response.status_code, 200)

        self.vote.refresh_from_db()
        self.assertEqual(self.vote.user, self.user)
        self.assertEqual(self.vote.meme, original_meme)
        self.assertEqual(self.vote.score, new_score)
        self.assertEqual(self.vote.submission_count, expected_new_submission_count)
