from django.urls import reverse_lazy

from apps.users.tests.factories import UserFactory
from meme_wars.tests import APITestCase


class TestLogoutAPIView(APITestCase):
    logout_url_path = reverse_lazy("api:users:logout")

    def test_should_return_response_401_when_authentication_headers_are_invalid(self):
        self.assertProtectedGETEndpoint(url_path=self.logout_url_path)

    def test_should_return_response_200_and_delete_auth_token(self):
        user = UserFactory()
        self.authenticate(user=user)
        user.refresh_from_db()
        self.assertIsNotNone(user.auth_token)
        response = self.client.get(path=self.logout_url_path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Success"})
        user.refresh_from_db()
        self.assertIsNone(getattr(user, "auth_token", None))
