from django.urls import reverse_lazy

from apps.common.tests import APITestCase
from apps.users.tests.factories import UserFactory
from apps.wars.models import War
from apps.wars.serializers import WarSerializer
from apps.wars.tests.factories import WarFactory


class TestWarViewSet(APITestCase):
    list_url_path = reverse_lazy('api:wars:wars-list')

    def setUp(self) -> None:
        super().setUp()
        WarFactory(phase=War.Phases.PREPARATION)
        WarFactory(phase=War.Phases.SUBMISSION)
        WarFactory(phase=War.Phases.VOTING)
        WarFactory(phase=War.Phases.FINISHED)

    def test_should_return_response_401_for_list_endpoint_when_authentication_headers_are_invalid(self):
        self.assertProtectedGETEndpoint(url_path=self.list_url_path)

    def test_should_return_all_wars(self):
        self.authenticate(user=UserFactory())
        response = self.client.get(path=self.list_url_path)
        serializer = WarSerializer(instance=War.objects.order_by('-created').all(), many=True)
        self.assertListResponse(response=response, expected_items=serializer.data)
