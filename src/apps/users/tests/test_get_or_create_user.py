from unittest.mock import patch

from apps.users.authentication import GoogleUser
from apps.users.models import User, UserSettings
from apps.users.tests.factories import GoogleUserFactory, UserFactory
from apps.users.utils import get_or_create_user
from meme_wars.tests.test_case import TestCase


class TestGetOrCreateUser(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.google_user = GoogleUserFactory(
            email="jon.snow@winterfell.com",
            given_name="Jon",
            family_name="Snow",
            picture="https://mock-google-domain/jon-snow.jpg",
        )

        self.validate_email_patcher = patch.object(UserSettings, "validate_email")
        self.mock_validate_email = self.validate_email_patcher.start()

    def test_should_create_user_when_they_do_not_exist(self):
        self.assertFalse(User.objects.exists())

        user, is_created = get_or_create_user(google_user=self.google_user)

        self.assertTrue(is_created)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqualUser(user, self.google_user)

    def test_should_update_and_get_user_when_they_exist(self):
        exiting_user = UserFactory(
            first_name="Miki", last_name="Mikanović", image_url="https://mock-google-domain/miki-mikanovic.jpg"
        )
        self.google_user.email = exiting_user.email
        self.assertEqual(User.objects.count(), 1)

        user, is_created = get_or_create_user(google_user=self.google_user)

        self.assertFalse(is_created)
        self.assertEqual(user, exiting_user)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqualUser(user, self.google_user)

    def assertEqualUser(self, user: User, google_user: GoogleUser) -> None:
        self.assertEqual(user.email, google_user.email)
        self.assertEqual(user.first_name, google_user.given_name)
        self.assertEqual(user.last_name, google_user.family_name)
        self.assertEqual(user.image_url, google_user.picture)

    def tearDown(self) -> None:
        super().tearDown()
        self.validate_email_patcher.stop()
