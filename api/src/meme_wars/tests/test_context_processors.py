from decouple import config

from django.conf import settings

from apps.common.tests import TestCase
from meme_wars import context_processors


class TestIndexView(TestCase):

    def test_should_contain_environment_variable(self):
        context = context_processors.meme_wars(request=self.get_request_example())
        self.assertEqual(context.get('environment'), config('ENVIRONMENT'))

    def test_should_contain_app_url_variable(self):
        context = context_processors.meme_wars(request=self.get_request_example())
        self.assertEqual(context.get('app_url'), settings.CLIENT_APP_URL)
