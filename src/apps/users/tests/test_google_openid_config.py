from unittest.mock import patch

from apps.users.authentication import GoogleOpenIDConfig, google_openid_config
from meme_wars.tests.test_case import TestCase


class TestGoogleOpenIDConfig(TestCase):
    @patch.object(google_openid_config, "_fetch_google_openid_config")
    def test_init_google_openid_config_with_data_fetched_from_google(self, mock_fetch_google_openid_config):
        authorization_endpoint = "https://mock-google-domain/authorization-endpoint/"
        token_endpoint = "https://mock-google-domain/token-endpoint/"
        mock_fetch_google_openid_config.return_value = {
            "authorization_endpoint": authorization_endpoint,
            "token_endpoint": token_endpoint,
        }
        config = GoogleOpenIDConfig()
        self.assertEqual(config.authorization_endpoint, authorization_endpoint)
        self.assertEqual(config.token_endpoint, token_endpoint)
