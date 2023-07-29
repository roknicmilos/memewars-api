from django.urls import reverse_lazy

from apps.users.tests.factories import UserFactory
from apps.wars.models import Meme, Vote, War
from apps.wars.serializers import VoteSerializer
from apps.wars.tests.factories import MemeFactory, VoteFactory, WarFactory
from meme_wars.tests import APITestCase


class TestVoteListCreateAPIView(APITestCase):
    url_path = reverse_lazy("api:votes:index")

    def setUp(self) -> None:
        super().setUp()
        war = WarFactory(phase=War.Phases.VOTING)
        self.user = UserFactory()
        self.meme = MemeFactory(war=war)
        self.valid_data = {
            "meme": self.meme.pk,
            "score": 5,
        }

    def test_list_endpoint_should_return_response_401_when_authentication_headers_are_invalid(self):
        self.assertProtectedGETEndpoint(url_path=self.url_path)

    def test_list_endpoint_should_return_all_votes(self):
        self.authenticate(user=self.user)
        VoteFactory.create_batch(size=3)
        response = self.client.get(path=self.url_path)
        serializer = VoteSerializer(
            instance=Vote.objects.all().order_by("-created"), many=True, context={"request": response.wsgi_request}
        )
        self.assertListResponse(response=response, serializer=serializer)

    def test_list_endpoint_should_return_filtered_votes(self):
        self.authenticate(user=self.user)

        user_votes = VoteFactory.create_batch(size=5, user=self.user)
        first_three_user_votes = user_votes[:3]

        war = WarFactory()
        for vote in first_three_user_votes:
            vote.meme.update(war=war)

        # 3 Additional Votes that do not belong to the authenticated User:
        other_votes = VoteFactory.create_batch(size=3, meme=MemeFactory(war=war))

        meme = MemeFactory(war=war)
        first_three_user_votes[0].update(meme=meme)
        other_votes[0].update(meme=meme)
        meme_votes = [first_three_user_votes[0], other_votes[0]]

        war_votes = [*first_three_user_votes, *other_votes]

        # When Votes are filtered by User:
        response = self.client.get(path=f"{self.url_path}?user={self.user.pk}")
        sorted_user_votes = sorted(user_votes, key=lambda obj: obj.created, reverse=True)
        serializer = VoteSerializer(instance=sorted_user_votes, many=True, context={"request": response.wsgi_request})
        self.assertListResponse(response=response, serializer=serializer)

        # When Votes are filtered by Meme:
        response = self.client.get(path=f"{self.url_path}?meme={meme.pk}")
        sorted_meme_votes = sorted(meme_votes, key=lambda obj: obj.created, reverse=True)
        serializer = VoteSerializer(instance=sorted_meme_votes, many=True, context={"request": response.wsgi_request})
        self.assertListResponse(response=response, serializer=serializer)

        # When Votes are filtered by War:
        response = self.client.get(path=f"{self.url_path}?war={war.pk}")
        sorted_war_votes = sorted(war_votes, key=lambda obj: obj.created, reverse=True)
        serializer = VoteSerializer(instance=sorted_war_votes, many=True, context={"request": response.wsgi_request})
        self.assertListResponse(response=response, serializer=serializer)

        # When Votes are filtered by User and Meme:
        response = self.client.get(path=f"{self.url_path}?user={self.user.pk}&meme={meme.pk}")
        serializer = VoteSerializer(
            instance=[first_three_user_votes[0]], many=True, context={"request": response.wsgi_request}
        )
        self.assertListResponse(response=response, serializer=serializer)

        # When Votes are filtered by User and War:
        response = self.client.get(path=f"{self.url_path}?user={self.user.pk}&war={war.pk}")
        ordered_first_three_user_votes = sorted(first_three_user_votes, key=lambda obj: obj.created, reverse=True)
        serializer = VoteSerializer(
            instance=ordered_first_three_user_votes, many=True, context={"request": response.wsgi_request}
        )
        self.assertListResponse(response=response, serializer=serializer)

    def test_create_endpoint_should_return_response_401_when_authentication_headers_are_invalid(self):
        self.assertProtectedPOSTEndpoint(url_path=self.url_path, data=self.valid_data)

    def test_create_endpoint_should_return_response_400_when_request_data_is_invalid(self):
        self.authenticate(user=self.user)

        # When Meme does not exist:
        missing_meme_pk = Meme.objects.latest("pk").pk + 1
        self.assertFalse(Meme.objects.filter(pk=missing_meme_pk).exists())
        data = {
            **self.valid_data,
            "meme": missing_meme_pk,
        }
        expected_errors = {
            "meme": [
                f'Invalid pk "{missing_meme_pk}" - object does not exist.',
            ],
        }
        self.assertBadRequestResponse(data=data, errors=expected_errors)

        # When Meme belongs to a War that is no in Voting phase:
        for phase in War.Phases:
            if phase is War.Phases.VOTING:
                continue
            war = WarFactory(phase=phase)
            meme = MemeFactory(war=war)
            data = {
                **self.valid_data,
                "meme": meme.pk,
            }
            expected_errors = {
                "meme": [
                    f'Meme must be in a war that is in "{War.Phases.VOTING.label}" phase',
                ],
            }
            self.assertBadRequestResponse(data=data, errors=expected_errors)

        # When Vote is less than 1:
        data = {
            **self.valid_data,
            "score": 0,
        }
        expected_errors = {
            "score": [
                "Ensure this value is greater than or equal to 1.",
            ],
        }
        self.assertBadRequestResponse(data=data, errors=expected_errors)

        # When Vote is more than 10:
        data = {
            **self.valid_data,
            "score": 11,
        }
        expected_errors = {
            "score": [
                "Ensure this value is less than or equal to 10.",
            ],
        }
        self.assertBadRequestResponse(data=data, errors=expected_errors)

    def test_create_endpoint_should_create_vote_and_return_response_201_when_request_data_is_valid(self):
        self.authenticate(user=self.user)
        self.assertFalse(Vote.objects.exists())

        response = self.client.post(path=self.url_path, data=self.valid_data)
        self.assertEqual(response.status_code, 201)

        vote = Vote.objects.first()
        self.assertIsNotNone(vote)
        self.assertEqual(vote.user, self.user)
        self.assertEqual(vote.meme, self.meme)
        self.assertEqual(vote.score, self.valid_data["score"])
        self.assertEqual(vote.submission_count, 1)

        serializer = VoteSerializer(instance=vote, context={"request": response.wsgi_request})
        self.assertEqual(response.json(), serializer.data)

    def test_update_endpoint_should_return_response_405(self):
        self.authenticate(user=self.user)
        response = self.client.put(path=self.url_path, data={})
        self.assertEqual(response.status_code, 405)
