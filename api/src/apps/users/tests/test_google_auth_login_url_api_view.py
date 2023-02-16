from unittest.mock import patch

from rest_framework.reverse import reverse

from apps.common.tests import TestCase
from apps.users.authentication import google_auth


class TestGoogleAuthLoginUrlAPIView(TestCase):

    @patch.object(google_auth, 'get_login_url')
    def test_should_return_google_login_url(self, mock_get_login_url):
        mock_get_login_url.return_value = 'https://mock-google/login-url'
        response = self.client.get(path=reverse('api:google_auth:login_url'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'url': mock_get_login_url.return_value})
