from django.urls import reverse_lazy

from apps.common.tests.fixtures import get_image_file_example
from apps.users.tests.factories import UserFactory
from apps.wars.models import Meme, War
from apps.wars.serializers import MemeSerializer
from apps.wars.tests.factories import MemeFactory, VoteFactory, WarFactory
from meme_wars.tests import APITestCase


class TestMemeListCreateAPIView(APITestCase):
    url_path = reverse_lazy("api:memes:index")

    def setUp(self) -> None:
        super().setUp()
        self.user = UserFactory()
        self.war_in_preparation_phase = WarFactory(phase=War.Phases.PREPARATION)
        self.war_in_submission_phase = WarFactory(phase=War.Phases.SUBMISSION)
        self.war_in_voting_phase = WarFactory(phase=War.Phases.VOTING)
        self.war_in_finished_phase = WarFactory(phase=War.Phases.FINISHED)
        self.all_wars = [
            self.war_in_preparation_phase,
            self.war_in_submission_phase,
            self.war_in_voting_phase,
            self.war_in_finished_phase,
        ]
        self.valid_data = {
            "image": get_image_file_example(),
            "war": self.war_in_submission_phase.pk,
        }

    def test_list_endpoint_should_return_response_401_when_authentication_headers_are_invalid(self):
        self.assertProtectedGETEndpoint(url_path=self.url_path)

    def test_list_endpoint_should_return_all_memes_automatically_filtered_by_approval_status(self):
        for war in self.all_wars:
            MemeFactory(war=war, approval_status=Meme.ApprovalStatuses.PENDING)
            MemeFactory(war=war, approval_status=Meme.ApprovalStatuses.REJECTED)
            MemeFactory(war=war, approval_status=Meme.ApprovalStatuses.APPROVED)
            MemeFactory(war=war, approval_status=Meme.ApprovalStatuses.PENDING, user=self.user)
            MemeFactory(war=war, approval_status=Meme.ApprovalStatuses.REJECTED, user=self.user)
            MemeFactory(war=war, approval_status=Meme.ApprovalStatuses.APPROVED, user=self.user)

        self.authenticate(user=self.user)

        # When all wars do not require meme approval:
        first_page_response = self.client.get(path=self.url_path)
        second_page_response = self.client.get(path=f"{self.url_path}?page=2")

        self.assertEqual(first_page_response.status_code, 200)
        self.assertEqual(second_page_response.status_code, 200)
        results = first_page_response.json()["results"] + second_page_response.json()["results"]
        # Expected memes:
        #   0 from the war in PREPARATION phase
        #   3 from the war in SUBMISSION phase (authenticated user memes only, regardless of approval status)
        #   6 from the war in VOTING phase (all memes)
        #   6 from the war in FINISHED phase (all memes)
        self.assertEqual(len(results), 15)
        for meme_dict in results:
            # There shouldn't be a meme from the war that's in the PREPARATION phase:
            self.assertNotEqual(meme_dict["war"], self.war_in_preparation_phase.pk)
            # If the meme is from the war that's in SUBMISSION phase,
            # it should belong to the authenticated user:
            if meme_dict["war"] == self.war_in_submission_phase.pk:
                self.assertEqual(meme_dict["user"], self.user.pk)

        # When all wars require meme approval:
        for war in self.all_wars:
            war.update(requires_meme_approval=True)

        response = self.client.get(path=self.url_path)

        self.assertEqual(response.status_code, 200)
        results = response.json()["results"]
        # Expected memes:
        #   0 from the war in PREPARATION phase
        #   3 from the war in SUBMISSION phase (authenticated user memes only, regardless of approval status)
        #   2 from the war in VOTING phase (approved memes only)
        #   2 from the war in FINISHED phase (approved memes only)
        self.assertEqual(len(results), 7)
        for meme_dict in results:
            # There shouldn't be a meme from the war that's in the PREPARATION phase:
            self.assertNotEqual(meme_dict["war"], self.war_in_preparation_phase.pk)
            # If the meme is from the war that's in SUBMISSION phase,
            # it should belong to the authenticated user:
            if meme_dict["war"] == self.war_in_submission_phase.pk:
                self.assertEqual(meme_dict["user"], self.user.pk)
            else:
                self.assertEqual(meme_dict["approval_status"], Meme.ApprovalStatuses.APPROVED.value)

    def test_list_endpoint_should_return_all_memes_ordered_by_correct_fields(self):
        war = WarFactory(phase=War.Phases.VOTING)

        meme_a = MemeFactory(war=war)
        VoteFactory(meme=meme_a, score=8)  # 1

        meme_b = MemeFactory(war=war)
        VoteFactory(meme=meme_b, score=7)  # 3

        meme_c = MemeFactory(war=war)
        VoteFactory(meme=meme_c, score=5)  # 5

        meme_d = MemeFactory(war=war)
        VoteFactory(meme=meme_d, score=6)  # 4

        meme_e = MemeFactory(war=war)
        VoteFactory(meme=meme_e, score=7)  # 2

        self.authenticate(user=self.user)
        url_path = f"{self.url_path}?war={war.pk}"

        # When war is in not the finished phase, memes should be
        # ordered by creation datetime:
        response = self.client.get(path=url_path)
        self.assertEqual(response.status_code, 200)
        results = response.json()["results"]
        self.assertEqual(results[0]["id"], meme_e.pk)
        self.assertEqual(results[1]["id"], meme_d.pk)
        self.assertEqual(results[2]["id"], meme_c.pk)
        self.assertEqual(results[3]["id"], meme_b.pk)
        self.assertEqual(results[4]["id"], meme_a.pk)

        # When war is in the finished phase, meme score should have
        # ordering priority over creation datetime:
        war.update(phase=War.Phases.FINISHED)
        response = self.client.get(path=url_path)
        self.assertEqual(response.status_code, 200)
        results = response.json()["results"]
        self.assertEqual(results[0]["id"], meme_a.pk)
        self.assertEqual(results[1]["id"], meme_e.pk)
        self.assertEqual(results[2]["id"], meme_b.pk)
        self.assertEqual(results[3]["id"], meme_d.pk)
        self.assertEqual(results[4]["id"], meme_c.pk)

    def test_list_endpoint_should_return_memes_filtered_by_war(self):
        self.authenticate(user=self.user)
        MemeFactory.create_batch(size=3, war=self.war_in_voting_phase)
        MemeFactory.create_batch(size=2, war=self.war_in_finished_phase)
        response = self.client.get(path=f"{self.url_path}?war={self.war_in_voting_phase.pk}")
        serializer = MemeSerializer(
            instance=self.war_in_voting_phase.memes.order_by("-created"),
            many=True,
            context={"request": response.wsgi_request},
        )
        self.assertListResponse(response=response, serializer=serializer)

        # When war requires meme approval:
        self.war_in_voting_phase.update(requires_meme_approval=True)
        self.war_in_voting_phase.memes.first().update(approval_status=Meme.ApprovalStatuses.APPROVED)
        response = self.client.get(path=f"{self.url_path}?war={self.war_in_voting_phase.pk}")
        serializer = MemeSerializer(
            instance=[self.war_in_voting_phase.memes.first()], many=True, context={"request": response.wsgi_request}
        )
        self.assertListResponse(response=response, serializer=serializer)

    def test_create_endpoint_should_return_response_401_when_authentication_headers_are_invalid(self):
        self.assertProtectedPOSTEndpoint(url_path=self.url_path, data=self.valid_data)

    def test_create_endpoint_should_return_response_400_when_request_data_is_invalid(self):
        self.authenticate(user=self.user)

        # When War does not exist:
        missing_war_pk = War.objects.latest("pk").pk + 1
        data = {
            **self.valid_data,
            "war": missing_war_pk,
        }
        expected_errors = {
            "war": [
                f'Invalid pk "{missing_war_pk}" - object does not exist.',
            ],
        }
        self.assertBadRequestResponse(data=data, errors=expected_errors)

        # When War is not in submission phase:
        for war in [self.war_in_preparation_phase, self.war_in_voting_phase, self.war_in_finished_phase]:
            data["war"] = war.pk
            # Make sure image file is fresh and valid for each request:
            data["image"] = get_image_file_example()
            expected_errors = {
                "war": [
                    'War must be in "Submission" phase',
                ],
            }
            self.assertBadRequestResponse(data=data, errors=expected_errors)

        # When image is invalid:
        data = {
            **self.valid_data,
            "image": "not-an-image",
        }
        expected_errors = {
            "image": [
                "The submitted data was not a file. Check the encoding type on the form.",
            ],
        }
        self.assertBadRequestResponse(data=data, errors=expected_errors)

    def test_create_endpoint_should_create_meme_and_return_response_201_when_meme_is_valid(self):
        self.authenticate(user=self.user)
        self.assertFalse(Meme.objects.exists())
        response = self.client.post(path=self.url_path, data=self.valid_data)
        self.assertEqual(response.status_code, 201)
        meme = Meme.objects.first()
        self.assertIsNotNone(meme)
        self.assertEqual(meme.war, self.war_in_submission_phase)
        self.assertEqual(meme.user, self.user)
        self.assertEqual(meme.approval_status, Meme.ApprovalStatuses.PENDING)
        serializer = MemeSerializer(instance=meme, context={"request": response.wsgi_request})
        # serializer.data['image'] is an absolute URL, and it should contain meme.image.url path:
        for key, value in response.json().items():
            if key == "image":
                self.assertTrue(serializer.data["image"].endswith(meme.image.url))
                continue
            self.assertEqual(value, serializer.data[key])

    def test_create_endpoint_should_return_response_400_when_meme_upload_limit_is_reached(self):
        self.authenticate(user=self.user)
        self.war_in_submission_phase.update(meme_upload_limit=1)
        MemeFactory(war=self.war_in_submission_phase, user=self.user)
        expected_errors = {
            "ALL": [
                "This user already reached Meme upload limit in this war.",
            ],
            "code": "meme_upload_limit_reached",
        }
        self.assertBadRequestResponse(data=self.valid_data, errors=expected_errors)
