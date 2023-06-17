from django.conf import settings

from meme_wars.tests.test_case import TestCase
from meme_wars.utils import build_absolute_admin_uri


class TestBuildAbsoluteAdminURI(TestCase):

    def test_should_build_absolute_admin_uri(self):
        absolute_uri = build_absolute_admin_uri(view_name='admin:index')
        self.assertTrue(absolute_uri.startswith(settings.ADMIN_URL))
