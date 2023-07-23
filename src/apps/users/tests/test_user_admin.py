from django.contrib.admin.sites import site as admin_site

from apps.users.admin import UserAdmin
from apps.users.models import User
from apps.users.tests.factories import UserFactory
from meme_wars.tests.test_case import TestCase


class TestUserAdmin(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.user_admin = UserAdmin(model=User, admin_site=admin_site)

    def test_should_return_inlines_when_editing_user(self):
        inlines = self.user_admin.get_inlines(request=self.get_request_example())
        self.assertEqual(inlines, ())

    def test_should_return_empty_tuple_instead_of_inlines_when_adding_user(self):
        inlines = self.user_admin.get_inlines(request=self.get_request_example(), obj=UserFactory())
        self.assertEqual(inlines, self.user_admin.inlines)

    def test_queryset_should_contain_email_deterministic_annotation(self):
        self.create_and_login_superuser()
        UserFactory.create_batch(size=2)

        queryset = self.user_admin.get_queryset(request=self.get_request_example())
        annotated_values = [item.email_deterministic for item in queryset]

        user_emails = [user.email for user in User.objects.all()]
        self.assertEqual(sorted(annotated_values), sorted(user_emails))
