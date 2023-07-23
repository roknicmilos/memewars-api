from datetime import datetime

from freezegun import freeze_time

from apps.common.utils import FilePath
from meme_wars.tests.test_case import TestCase


class TestFilePath(TestCase):
    def test_should_append_timestamp_to_filepath(self):
        base_path = "/media/tests/"
        file_path_obj = FilePath(base_path=base_path)
        with freeze_time("2000-1-1"):
            now = str(datetime.now().timestamp()).replace(".", "_")
            file_path = file_path_obj(instance=None, filename="test-file.pdf")
        self.assertEqual(file_path, f"{base_path}test-file_{now}.pdf")
