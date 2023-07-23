from apps.common.tests.fixtures import get_image_file_example
from apps.common.utils import compress_image_file
from meme_wars.tests.test_case import TestCase


class TestCompressImageFile(TestCase):
    def test_should_shrink_image_memory_size_and_convert_it_to_jpeg(self):
        original_image = get_image_file_example()
        new_image = compress_image_file(image=original_image)
        self.assertLess(new_image.size, original_image.size)
