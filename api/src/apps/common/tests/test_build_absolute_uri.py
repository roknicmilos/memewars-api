from django.conf import settings

from apps.common.tests import TestCase
from apps.common.utils import build_absolute_uri


class TestBuildAbsoluteURI(TestCase):

    def test_should_build_absolute_uri(self):
        absolute_uri = build_absolute_uri(view_name='admin:index')
        self.assertTrue(absolute_uri.startswith(settings.HOST_URL))
