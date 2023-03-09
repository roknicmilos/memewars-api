import pytest
from unittest.mock import patch
from apps.common.tests import TestCase
from apps.users.authentication import GoogleUser
from apps.users.models import User, UserSettings
from apps.users.tests.factories import GoogleUserFactory, UserFactory
from apps.users.utils import get_or_create_user, google_auth


class TestGetOrCreateUser(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.get_google_user_patcher = patch.object(google_auth, 'get_user')
        self.mock_get_google_user = self.get_google_user_patcher.start()
        self.mock_get_google_user.return_value = GoogleUserFactory(
            email='jon.snow@winterfell.com',
            given_name='Jon',
            family_name='Snow',
            picture='https://mock-google-domain/jon-snow.jpg'
        )

        self.validate_email_patcher = patch.object(UserSettings, 'validate_email')
        self.mock_validate_email = self.validate_email_patcher.start()

    def test_should_create_user_when_they_do_not_exist(self):
        self.assertFalse(User.objects.exists())

        user, is_created = get_or_create_user(request=self.get_request_example())

        self.assertTrue(is_created)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqualUser(user, self.mock_get_google_user.return_value)

    def test_should_update_and_get_user_when_they_exist(self):
        exiting_user = UserFactory(
            first_name='Miki',
            last_name='Mikanović',
            image_url='https://mock-google-domain/miki-mikanovic.jpg'
        )
        self.mock_get_google_user.return_value.email = exiting_user.email
        self.assertEqual(User.objects.count(), 1)

        user, is_created = get_or_create_user(request=self.get_request_example())

        self.assertFalse(is_created)
        self.assertEqual(user, exiting_user)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqualUser(user, self.mock_get_google_user.return_value)

    @patch.object(UserSettings, 'validate_email')
    def test_should_not_create_user_when_email_validation_fails(self, mock_validate_email):
        error_message = 'Invalid email address'
        mock_validate_email.side_effect = Exception(error_message)

        with pytest.raises(expected_exception=Exception, match=error_message):
            get_or_create_user(request=self.get_request_example())

    def assertEqualUser(self, user: User, google_user: GoogleUser) -> None:
        self.assertEqual(user.email, google_user.email)
        self.assertEqual(user.first_name, google_user.given_name)
        self.assertEqual(user.last_name, google_user.family_name)
        self.assertEqual(user.image_url, google_user.picture)

    def tearDown(self) -> None:
        super().tearDown()
        self.get_google_user_patcher.stop()
        self.validate_email_patcher.stop()
