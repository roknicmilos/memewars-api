from django.conf import settings

from meme_wars.tests.test_case import TestCase
from meme_wars.utils import build_absolute_api_uri


class TestBuildAbsoluteAPIURI(TestCase):

    def test_should_build_absolute_api_uri(self):
        absolute_uri = build_absolute_api_uri(view_name='index')
        self.assertTrue(absolute_uri.startswith(settings.API_URL))
