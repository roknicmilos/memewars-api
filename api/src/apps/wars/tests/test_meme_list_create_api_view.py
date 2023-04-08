from django.urls import reverse_lazy
from apps.common.tests import APITestCase
from apps.common.tests.fixtures import get_image_file_example
from apps.users.tests.factories import UserFactory
from apps.wars.models import Meme, War
from apps.wars.serializers import MemeSerializer
from apps.wars.tests.factories import MemeFactory, WarFactory


class TestMemeListCreateAPIView(APITestCase):
    url_path = reverse_lazy('api:memes:index')

    def setUp(self) -> None:
        super().setUp()
        self.user = UserFactory()
        self.wars = [WarFactory(phase=phase) for phase in War.Phases]
        self.war_in_submission_phase = next(war for war in self.wars if war.phase is War.Phases.SUBMISSION)
        self.valid_data = {
            'image': get_image_file_example(),
            'war': self.war_in_submission_phase.pk,
            'user': self.user.pk,
        }

    def test_list_endpoint_should_return_response_401_when_authentication_headers_are_invalid(self):
        self.assertProtectedGETEndpoint(url_path=self.url_path)

    def test_list_endpoint_should_return_all_memes(self):
        self.authenticate(user=self.user)
        response = self.client.get(path=self.url_path)
        serializer = MemeSerializer(instance=Meme.objects.order_by('-created').all(), many=True)
        self.assertListResponse(response=response, serializer=serializer)

    def test_list_endpoint_should_return_memes_filtered_by_war(self):
        self.authenticate(user=self.user)
        MemeFactory.create_batch(size=3, war=self.wars[0])
        MemeFactory.create_batch(size=2, war=self.wars[1])
        response = self.client.get(path=f'{self.url_path}?war={self.wars[0].pk}')
        serializer = MemeSerializer(instance=Meme.objects.order_by('-created').filter(war=self.wars[0]), many=True)
        self.assertListResponse(response=response, serializer=serializer)

    def test_list_endpoint_should_return_memes_filtered_by_approval_status(self):
        self.authenticate(user=self.user)
        MemeFactory.create_batch(size=2, approval_status=Meme.ApprovalStatuses.PENDING)
        MemeFactory.create_batch(size=3, approval_status=Meme.ApprovalStatuses.APPROVED)
        MemeFactory.create_batch(size=4, approval_status=Meme.ApprovalStatuses.REJECTED)

        # "Pending" approval status:
        response = self.client.get(path=f'{self.url_path}?approval_status={Meme.ApprovalStatuses.PENDING}')
        queryset = Meme.objects.order_by('-created').filter(approval_status=Meme.ApprovalStatuses.PENDING)
        serializer = MemeSerializer(instance=queryset, many=True)
        self.assertListResponse(response=response, serializer=serializer)

        # "Approved" approval status:
        response = self.client.get(path=f'{self.url_path}?approval_status={Meme.ApprovalStatuses.APPROVED}')
        queryset = Meme.objects.order_by('-created').filter(approval_status=Meme.ApprovalStatuses.APPROVED)
        serializer = MemeSerializer(instance=queryset, many=True)
        self.assertListResponse(response=response, serializer=serializer)

        # "Rejected" approval status:
        response = self.client.get(path=f'{self.url_path}?approval_status={Meme.ApprovalStatuses.REJECTED}')
        queryset = Meme.objects.order_by('-created').filter(approval_status=Meme.ApprovalStatuses.REJECTED)
        serializer = MemeSerializer(instance=queryset, many=True)
        self.assertListResponse(response=response, serializer=serializer)

    def test_post_endpoint_should_return_response_401_when_authentication_headers_are_invalid(self):
        self.assertProtectedPOSTEndpoint(url_path=self.url_path, data=self.valid_data)

    def test_post_endpoint_should_return_response_400_when_meme_is_invalid(self):
        self.authenticate(user=self.user)

        # When War does not exist:
        missing_war_pk = War.objects.latest('pk').pk + 1
        data = {
            **self.valid_data,
            'war': missing_war_pk,
        }
        expected_errors = {
            'war': [f'Invalid pk "{missing_war_pk}" - object does not exist.', ],
        }
        self.assertBadRequestResponse(data=data, errors=expected_errors)

        # When War is not in submission phase:
        for war in self.wars:
            if war.phase is War.Phases.SUBMISSION:
                continue
            data['war'] = war.pk
            # Make sure image file is fresh and valid for each request:
            data['image'] = get_image_file_example()
            expected_errors = {
                'war': ['War must be in "Submission" phase', ],
            }
            self.assertBadRequestResponse(data=data, errors=expected_errors)

        # When image is invalid
        data = {
            **self.valid_data,
            'image': 'not-an-image',
        }
        expected_errors = {
            'image': ['The submitted data was not a file. Check the encoding type on the form.', ],
        }
        self.assertBadRequestResponse(data=data, errors=expected_errors)

    def assertBadRequestResponse(self, data: dict, errors: dict[str, list[str]]) -> None:
        response = self.client.post(path=self.url_path, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), errors)

    def test_post_endpoint_should_create_meme_and_return_response_201_when_meme_is_valid(self):
        self.authenticate(user=self.user)
        self.assertFalse(Meme.objects.exists())
        response = self.client.post(path=self.url_path, data=self.valid_data)
        self.assertEqual(response.status_code, 201)
        meme = Meme.objects.first()
        self.assertIsNotNone(meme)
        self.assertEqual(meme.war, self.war_in_submission_phase)
        self.assertEqual(meme.user, self.user)
        self.assertEqual(meme.approval_status, Meme.ApprovalStatuses.PENDING)
        serializer = MemeSerializer(instance=meme)
        # serializer.data['image'] is an absolute URL, and it should contain meme.image.url path:
        self.assertTrue(serializer.data['image'].endswith(meme.image.url))
