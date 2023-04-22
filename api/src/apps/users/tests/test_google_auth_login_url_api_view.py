from unittest.mock import patch

from rest_framework.reverse import reverse

from apps.common.tests import TestCase
from apps.users.authentication import google_auth


class TestGoogleAuthLoginURLAPIView(TestCase):

    @patch.object(google_auth, 'get_login_url')
    def test_should_redirect_to_google_login_url(self, mock_get_login_url):
        mock_get_login_url.return_value = 'https://mock-google/login'
        response = self.client.get(path=reverse('api:users:google_auth:login'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, mock_get_login_url.return_value)
