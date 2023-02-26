from django.urls import reverse, reverse_lazy

from apps.common.tests import APITestCase
from apps.users.tests.factories import UserFactory
from apps.wars.models import War
from apps.wars.serializers import WarSerializer
from apps.wars.tests.factories import WarFactory


class TestWarViewSet(APITestCase):
    list_url_path = reverse_lazy('api:wars:wars-list')

    def setUp(self) -> None:
        super().setUp()

        self.user = UserFactory()

        self.first_war = WarFactory(phase=War.Phases.PREPARATION)
        WarFactory(phase=War.Phases.SUBMISSION)
        WarFactory(phase=War.Phases.VOTING)
        WarFactory(phase=War.Phases.FINISHED)

        self.retrieve_url_path = reverse('api:wars:wars-detail', args=(self.first_war.pk,))

    def test_should_return_response_401_for_list_endpoint_when_authentication_headers_are_invalid(self):
        self.assertProtectedGETEndpoint(url_path=self.retrieve_url_path)

    def test_should_return_all_wars(self):
        self.authenticate(user=UserFactory())
        response = self.client.get(path=self.list_url_path)
        serializer = WarSerializer(instance=War.objects.order_by('-created').all(), many=True)
        self.assertListResponse(response=response, expected_items=serializer.data)

    def test_should_return_response_401_for_retrieve_endpoint_when_authentication_headers_are_invalid(self):
        self.assertProtectedGETEndpoint(url_path=self.retrieve_url_path)

    def test_should_return_single_war(self):
        self.authenticate(user=UserFactory())
        response = self.client.get(path=self.retrieve_url_path)
        serializer = WarSerializer(instance=self.first_war)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), serializer.data)

    def test_should_return_response_404_when_war_does_not_exist(self):
        non_existing_war_id = War.objects.last().pk + 1
        self.assertFalse(War.objects.filter(pk=non_existing_war_id).exists())
        self.authenticate(user=UserFactory())
        url_path = reverse('api:wars:wars-detail', args=(non_existing_war_id,))
        response = self.client.get(path=url_path)
        self.assertEqual(response.json(), {'message': 'Not fount'})
