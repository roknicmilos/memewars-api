from unittest import TestCase

from apps.users.models import User


class TestUser(TestCase):

    def tearDown(self) -> None:
        super().tearDown()
        User.objects.all().delete()

    def test_should_create_user(self):
        kwargs = {
            'email': 'example@example.com',
            'password': 'pass4user',
            'first_name': 'Jon',
            'last_name': 'Snow',
        }
        self.assertFalse(User.objects.exists())

        user = User.objects.create_user(**kwargs)

        self.assertCommonUserKwargs(user=user, expected_kwargs=kwargs)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_should_create_superuser(self):
        kwargs = {
            'email': 'example@example.com',
            'password': 'pass4user',
            'first_name': 'Jon',
            'last_name': 'Snow',
        }
        self.assertFalse(User.objects.exists())

        user = User.objects.create_superuser(**kwargs)

        self.assertCommonUserKwargs(user=user, expected_kwargs=kwargs)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def assertCommonUserKwargs(self, user: User, expected_kwargs: dict) -> None:
        self.assertEqual(user.email, expected_kwargs['email'])
        self.assertTrue(user.check_password(expected_kwargs['password']))
        self.assertEqual(user.first_name, expected_kwargs['first_name'])
        self.assertEqual(user.last_name, expected_kwargs['last_name'])
        self.assertIsNone(user.username)
        self.assertTrue(user.is_active)
