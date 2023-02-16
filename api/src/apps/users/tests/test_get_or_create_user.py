from apps.common.tests import TestCase
from apps.users.authentication import GoogleUser
from apps.users.models import User
from apps.users.tests.factories import GoogleUserFactory, UserFactory
from apps.users.utils import get_or_create_user


class TestGetOrCreateUser(TestCase):

    def test_should_create_user_when_they_do_not_exist(self):
        google_user = GoogleUserFactory()
        self.assertFalse(User.objects.exists())

        user, is_created = get_or_create_user(google_user=google_user)

        self.assertTrue(is_created)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqualUser(user, google_user)

    def test_should_update_and_get_user_when_they_exist(self):
        exiting_user = UserFactory(
            first_name='Miki',
            last_name='Mikanović',
            image_url='https://mock-google-domain/miki-mikanovic.jpg'
        )
        google_user = GoogleUserFactory(
            email=exiting_user.email,
            given_name='Jon',
            family_name='Snow',
            picture='https://mock-google-domain/jon-snow.jpg'
        )
        self.assertEqual(User.objects.count(), 1)

        user, is_created = get_or_create_user(google_user=google_user)

        self.assertFalse(is_created)
        self.assertEqual(user, exiting_user)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqualUser(user, google_user)

    def assertEqualUser(self, user: User, google_user: GoogleUser) -> None:
        self.assertEqual(user.email, google_user.email)
        self.assertEqual(user.first_name, google_user.given_name)
        self.assertEqual(user.last_name, google_user.family_name)
        self.assertEqual(user.image_url, google_user.picture)
