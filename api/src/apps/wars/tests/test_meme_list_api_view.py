from django.urls import reverse_lazy

from apps.common.tests import APITestCase
from apps.users.tests.factories import UserFactory
from apps.wars.models import Meme
from apps.wars.serializers import MemeSerializer
from apps.wars.tests.factories import MemeFactory, WarFactory


class TestMemeListAPIView(APITestCase):
    list_url_path = reverse_lazy('api:memes:list')

    def setUp(self) -> None:
        super().setUp()
        self.user = UserFactory()

    def test_should_return_response_401_when_authentication_headers_are_invalid(self):
        self.assertProtectedGETEndpoint(url_path=self.list_url_path)

    def test_should_return_all_memes(self):
        self.authenticate(user=self.user)
        response = self.client.get(path=self.list_url_path)
        serializer = MemeSerializer(instance=Meme.objects.order_by('-created').all(), many=True)
        self.assertListResponse(response=response, serializer=serializer)

    def test_should_return_memes_filtered_by_war(self):
        self.authenticate(user=self.user)
        first_war = WarFactory()
        MemeFactory.create_batch(size=3, war=first_war)
        second_war = WarFactory()
        MemeFactory.create_batch(size=2, war=second_war)
        response = self.client.get(path=f'{self.list_url_path}?war={first_war.pk}')
        serializer = MemeSerializer(instance=Meme.objects.order_by('-created').filter(war=first_war), many=True)
        self.assertListResponse(response=response, serializer=serializer)

    def test_should_return_memes_filtered_by_approval_status(self):
        self.authenticate(user=self.user)
        MemeFactory.create_batch(size=2, approval_status=Meme.ApprovalStatuses.PENDING)
        MemeFactory.create_batch(size=3, approval_status=Meme.ApprovalStatuses.APPROVED)
        MemeFactory.create_batch(size=4, approval_status=Meme.ApprovalStatuses.REJECTED)

        # "Pending" approval status:
        response = self.client.get(path=f'{self.list_url_path}?approval_status={Meme.ApprovalStatuses.PENDING}')
        queryset = Meme.objects.order_by('-created').filter(approval_status=Meme.ApprovalStatuses.PENDING)
        serializer = MemeSerializer(instance=queryset, many=True)
        self.assertListResponse(response=response, serializer=serializer)

        # "Approved" approval status:
        response = self.client.get(path=f'{self.list_url_path}?approval_status={Meme.ApprovalStatuses.APPROVED}')
        queryset = Meme.objects.order_by('-created').filter(approval_status=Meme.ApprovalStatuses.APPROVED)
        serializer = MemeSerializer(instance=queryset, many=True)
        self.assertListResponse(response=response, serializer=serializer)

        # "Rejected" approval status:
        response = self.client.get(path=f'{self.list_url_path}?approval_status={Meme.ApprovalStatuses.REJECTED}')
        queryset = Meme.objects.order_by('-created').filter(approval_status=Meme.ApprovalStatuses.REJECTED)
        serializer = MemeSerializer(instance=queryset, many=True)
        self.assertListResponse(response=response, serializer=serializer)
