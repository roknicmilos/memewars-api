from django.urls import reverse
from rest_framework.response import Response

from apps.common.tests import TestCase


class TestAPIIndexView(TestCase):

    def test_should_return_response_200_with_message(self):
        response = self.client.get(path=reverse('api:index'))
        self.assertIsInstance(response, Response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'This is the base URL for the Meme Wars API'})
