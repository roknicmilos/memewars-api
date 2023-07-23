from django.urls import reverse_lazy

from apps.users.tests.factories import UserFactory
from apps.wars.models import War
from apps.wars.serializers import WarSerializer
from apps.wars.tests.factories import WarFactory
from meme_wars.tests import APITestCase


class TestWarListAPIView(APITestCase):
    url_path = reverse_lazy("api:wars:index")

    def setUp(self) -> None:
        super().setUp()
        for phase in War.Phases:
            WarFactory(phase=phase)

    def test_list_endpoint_should_return_response_401_when_authentication_headers_are_invalid(self):
        self.assertProtectedGETEndpoint(url_path=self.url_path)

    def test_list_endpoint_should_return_all_wars(self):
        self.authenticate(user=UserFactory())
        response = self.client.get(path=self.url_path)
        serializer = WarSerializer(instance=War.objects.order_by("-created").all(), many=True)
        self.assertListResponse(response=response, serializer=serializer)
