from apps.users.models import UserSettings
from meme_wars.tests.test_case import TestCase


class TestUserSettings(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.user_settings = UserSettings.load()

    def test_should_raise_validation_error_when_email_is_not_allowed(self):
        self.assertEqual(self.user_settings.allowed_email_domains, [])
        self.assertEqual(self.user_settings.allowed_emails, [])
        with self.raisesDjangoValidationError(match="This email is not allowed", code="forbidden_email"):
            self.user_settings.validate_email(email="example@example.com")

    def test_should_not_raise_any_error_when_email_is_allowed(self):
        # When all domains are allowed:
        self.user_settings.update(allowed_email_domains=["*"])
        self.user_settings.validate_email(email="example@example.com")

        # When only specific domains are allowed:
        self.user_settings.update(allowed_email_domains=["example.com"])
        self.user_settings.validate_email(email="example@example.com")

        # When email address is not allowed by "allowed domain domains", but it is by "allowed emails":
        self.user_settings.update(allowed_emails=["example@secondexample.com"])
        self.user_settings.validate_email(email="example@secondexample.com")
