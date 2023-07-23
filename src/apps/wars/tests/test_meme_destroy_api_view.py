from django.urls import reverse

from apps.users.tests.factories import UserFactory
from apps.wars.models import Meme
from apps.wars.tests.factories import MemeFactory
from meme_wars.tests import APITestCase


class TestMemeDestroyAPIView(APITestCase):
    def test_destroy_endpoint_should_return_response_401_when_authentication_headers_are_invalid(self):
        meme = MemeFactory()
        url_path = reverse("api:memes:details", args=(meme.pk,))
        self.assertProtectedDELETEEndpoint(url_path=url_path)

    def test_destroy_endpoint_should_return_response_404_when_meme_does_not_exist(self):
        user = UserFactory()
        self.authenticate(user=user)
        self.assertFalse(Meme.objects.filter(pk=1).exists())
        url_path = reverse("api:memes:details", args=(1,))
        response = self.client.delete(path=url_path)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"message": "Not found"})

    def test_destroy_endpoint_should_return_response_404_when_meme_does_not_belong_to_authenticated_user(self):
        user = UserFactory()
        self.authenticate(user=user)
        meme = MemeFactory()
        self.assertNotEqual(user, meme.user)
        url_path = reverse("api:memes:details", args=(meme.pk,))
        response = self.client.delete(path=url_path)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"message": "Not found"})
        self.assertTrue(Meme.objects.filter(pk=meme.pk).exists())

    def test_destroy_endpoint_should_return_response_204_and_delete_meme(self):
        meme = MemeFactory()
        self.authenticate(user=meme.user)
        url_path = reverse("api:memes:details", args=(meme.pk,))
        response = self.client.delete(path=url_path)
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(response.content_type)
        self.assertEqual(response.content, b"")
        self.assertFalse(Meme.objects.filter(pk=meme.pk).exists())
