from django.urls import reverse_lazy

from apps.users.tests.factories import UserFactory
from apps.wars.models import War, Vote, Meme
from apps.wars.serializers import VoteSerializer
from apps.wars.tests.factories import MemeFactory, WarFactory, VoteFactory
from meme_wars.tests import APITestCase


class TestVoteListCreateAPIView(APITestCase):
    url_path = reverse_lazy('api:votes:index')

    def setUp(self) -> None:
        super().setUp()
        war = WarFactory(phase=War.Phases.VOTING)
        self.user = UserFactory()
        self.meme = MemeFactory(war=war)
        self.valid_data = {
            'meme': self.meme.pk,
            'score': 5,
        }

    def test_list_endpoint_should_return_response_401_when_authentication_headers_are_invalid(self):
        self.assertProtectedGETEndpoint(url_path=self.url_path)

    def test_list_endpoint_should_return_all_votes(self):
        self.authenticate(user=self.user)
        votes = VoteFactory.create_batch(size=3)
        response = self.client.get(path=self.url_path)
        serializer = VoteSerializer(instance=votes, many=True)
        self.assertListResponse(response=response, serializer=serializer)

    def test_list_endpoint_should_return_votes_filtered_by_voter(self):
        self.authenticate(user=self.user)
        user_votes = VoteFactory.create_batch(size=2, user=self.user)
        # 3 Additional Votes that do not belong to the authenticated User:
        VoteFactory.create_batch(size=3)
        serializer = VoteSerializer(instance=user_votes, many=True)
        response = self.client.get(path=f'{self.url_path}?user={self.user.pk}')
        self.assertListResponse(response=response, serializer=serializer)

    def test_create_endpoint_should_return_response_401_when_authentication_headers_are_invalid(self):
        self.assertProtectedPOSTEndpoint(url_path=self.url_path, data=self.valid_data)

    def test_create_endpoint_should_return_response_400_when_request_data_is_invalid(self):
        self.authenticate(user=self.user)

        # When Meme does not exist:
        missing_meme_pk = Meme.objects.latest('pk').pk + 1
        self.assertFalse(Meme.objects.filter(pk=missing_meme_pk).exists())
        data = {
            **self.valid_data,
            'meme': missing_meme_pk,
        }
        expected_errors = {
            'meme': [f'Invalid pk "{missing_meme_pk}" - object does not exist.', ],
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
                'meme': meme.pk,
            }
            expected_errors = {
                'meme': [f'Meme must be in a war that is in "{War.Phases.VOTING.label}" phase', ],
            }
            self.assertBadRequestResponse(data=data, errors=expected_errors)

        # When Vote is less than 1:
        data = {
            **self.valid_data,
            'score': 0,
        }
        expected_errors = {
            'score': ['Ensure this value is greater than or equal to 1.', ],
        }
        self.assertBadRequestResponse(data=data, errors=expected_errors)

        # When Vote is more than 10:
        data = {
            **self.valid_data,
            'score': 11,
        }
        expected_errors = {
            'score': ['Ensure this value is less than or equal to 10.', ],
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
        self.assertEqual(vote.score, self.valid_data['score'])
        self.assertEqual(vote.submission_count, 1)

        serializer = VoteSerializer(instance=vote)
        self.assertEqual(response.json(), serializer.data)
