from django.conf import settings

from meme_wars.tests.test_case import TestCase
from meme_wars.utils import build_absolute_uri


class TestBuildAbsoluteURI(TestCase):
    def test_should_build_absolute_uri(self):
        absolute_uri = build_absolute_uri(view_name="index")
        self.assertTrue(absolute_uri.startswith(settings.HOST_URL))
