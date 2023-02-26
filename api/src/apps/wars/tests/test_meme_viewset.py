from django.urls import reverse_lazy

from apps.common.tests import APITestCase
from apps.users.tests.factories import UserFactory
from apps.wars.models import Meme
from apps.wars.serializers import MemeSerializer
from apps.wars.tests.factories import MemeFactory, WarFactory


class TestMemeViewSet(APITestCase):
    list_url_path = reverse_lazy('api:wars:memes-list')

    def setUp(self) -> None:
        super().setUp()
        first_war = WarFactory()
        MemeFactory.create_batch(size=3, war=first_war)
        second_war = WarFactory()
        MemeFactory.create_batch(size=2, war=second_war)

    def test_should_return_response_401_for_list_endpoint_when_authentication_headers_are_invalid(self):
        self.assertProtectedGETEndpoint(url_path=self.list_url_path)

    def test_should_return_all_memes(self):
        self.authenticate(user=UserFactory())
        response = self.client.get(path=self.list_url_path)
        serializer = MemeSerializer(instance=Meme.objects.order_by('-created').all(), many=True)
        self.assertListResponse(response=response, expected_items=serializer.data)
