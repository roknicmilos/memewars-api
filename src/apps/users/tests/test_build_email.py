from apps.users.tests.factories import GoogleUserFactory, UserFactory
from apps.users.tests.factories.utils import build_email
from meme_wars.tests.test_case import TestCase


class TestBuildEmail(TestCase):
    def test_should_build_user_email(self):
        user = UserFactory()
        email = build_email(user=user)
        email_parts = email.split("@")
        non_domain_parts = email_parts[0].split(".")
        self.assertEqual(len(non_domain_parts), 3)
        self.assertEqual(non_domain_parts[0], user.first_name)
        self.assertEqual(non_domain_parts[1], user.last_name)
        self.assertUUIDString(non_domain_parts[2])
        self.assertEqual(email_parts[1], "example.rs")

    def test_should_build_google_user_email(self):
        google_user = GoogleUserFactory()
        email = build_email(user=google_user)
        email_parts = email.split("@")
        non_domain_parts = email_parts[0].split(".")
        self.assertEqual(len(non_domain_parts), 3)
        self.assertEqual(non_domain_parts[0], google_user.given_name)
        self.assertEqual(non_domain_parts[1], google_user.family_name)
        self.assertUUIDString(non_domain_parts[2])
        self.assertEqual(email_parts[1], "example.rs")
