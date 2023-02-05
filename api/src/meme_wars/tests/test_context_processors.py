from os import getenv
from apps.common.tests import TestCase
from meme_wars import context_processors


class TestIndexView(TestCase):

    def test_should_contain_environment_variable(self):
        context = context_processors.meme_wars(request=self.request_example)
        self.assertEqual(context.get('environment'), getenv('ENVIRONMENT'))

    def test_should_contain_app_url_variable(self):
        context = context_processors.meme_wars(request=self.request_example)
        self.assertEqual(context.get('app_url'), getenv('APP_URL'))
