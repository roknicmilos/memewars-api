from django.urls import reverse

from apps.users.tests.factories import UserFactory
from apps.wars.models import War
from apps.wars.serializers import WarSerializer
from apps.wars.tests.factories import WarFactory
from meme_wars.tests import APITestCase


class TestWarRetrieveAPIView(APITestCase):
    def setUp(self) -> None:
        self.war = WarFactory()
        self.url_path = reverse("api:wars:details", args=(self.war.pk,))
        self.user = UserFactory()

    def test_retrieve_endpoint_should_return_response_401_when_authentication_headers_are_invalid(self):
        self.assertProtectedGETEndpoint(url_path=self.url_path)

    def test_retrieve_endpoint_should_return_response_404_when_war_does_not_exist(self):
        missing_war_id = War.objects.latest("pk").pk + 1
        self.assertFalse(War.objects.filter(pk=missing_war_id).exists())
        self.authenticate(user=self.user)
        url_path = reverse("api:wars:details", args=(missing_war_id,))
        response = self.client.get(path=url_path)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"message": "Not found"})

    def test_retrieve_endpoint_should_return_war(self):
        self.authenticate(user=self.user)
        response = self.client.get(path=self.url_path)
        self.assertEqual(response.status_code, 200)
        serializer = WarSerializer(instance=self.war)
        self.assertEqual(response.json(), serializer.data)
