from django.contrib.admin.sites import site as admin_site

from apps.users.admin import MemeAdminInline
from apps.users.models import User
from apps.users.tests.factories import UserFactory
from meme_wars.tests.test_case import TestCase


class TestMemeAdminInline(TestCase):
    def test_should_not_allow_to_add_new_objects(self):
        meme_admin_inline = MemeAdminInline(parent_model=User, admin_site=admin_site)
        self.assertFalse(meme_admin_inline.has_add_permission(request=self.get_request_example(), obj=UserFactory()))
