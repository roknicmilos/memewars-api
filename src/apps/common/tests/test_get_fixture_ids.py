from os.path import join

from django.conf import settings

from apps.common.utils import get_fixture_ids
from meme_wars.tests.test_case import TestCase


class TestGetFixtureIDs(TestCase):
    def test_should_return_fixture_ids_with_duplicates(self):
        fixtures_file_path = join(settings.PROJECT_ROOT, "apps", "common", "tests", "fixtures_example.yaml")
        ids = get_fixture_ids(fixtures_file_path=fixtures_file_path)
        self.assertEqual(ids, [1, 2, 2])
