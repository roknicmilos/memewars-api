from django.core.exceptions import ValidationError

from apps.common.tests import TestCase
from apps.users.models import UserSettings


class TestUserSettings(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.user_settings = UserSettings.load()

    def test_should_raise_validation_error_when_email_is_not_allowed(self):
        self.assertEqual(self.user_settings.allowed_email_domains, [])
        self.assertEqual(self.user_settings.allowed_emails, [])
        try:
            self.user_settings.validate_email(email='example@example.com')
        except ValidationError as error:
            self.assertEqual(error.code, 'forbidden_email')
            self.assertEqual(error.message, 'This email is not allowed')
        else:  # pragma: no cover
            self.fail('Did not raise ValidationError')

    def test_should_not_raise_any_error_when_email_is_allowed(self):
        self.user_settings.update(allowed_email_domains=['example.com'])
        self.assertEqual(self.user_settings.allowed_email_domains, ['example.com'])
        self.assertEqual(self.user_settings.allowed_emails, [])
        self.user_settings.validate_email(email='example@example.com')

        # When email address is not allowed by "allowed domain domains", but it is by "allowed emails":
        self.user_settings.update(allowed_emails=['example@secondexample.com'])
        self.user_settings.validate_email(email='example@secondexample.com')
