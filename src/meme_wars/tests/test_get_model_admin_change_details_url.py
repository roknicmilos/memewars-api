from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from meme_wars.tests.test_case import TestCase
from meme_wars.utils import get_model_admin_change_details_url


class TestGetModelAdminChangeDetailsUrl(TestCase):
    def test_should_return_empty_string_when_model_is_not_registered_on_admin_site(self):
        group = Group.objects.create(name="New group")
        url = get_model_admin_change_details_url(group)
        self.assertEqual(url, "")

    def test_should_return_url_when_model_is_registered_on_admin_site(self):
        user_class = get_user_model()
        user = user_class.objects.create()
        url = get_model_admin_change_details_url(user)
        self.assertEqual(url, f"/admin/users/user/{user.pk}/change/")
