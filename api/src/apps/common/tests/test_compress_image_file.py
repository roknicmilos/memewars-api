from os.path import join

from django.conf import settings
from django.core.files.images import ImageFile

from apps.common.tests import TestCase
from apps.common.utils import compress_image_file


class TestCompressImageFile(TestCase):

    def test_should_shrink_image_memory_size_and_convert_it_to_jpeg(self):
        image_path = join(settings.MEDIA_ROOT, 'fixtures', 'memes', 'meme_template_1.jpg')
        original_image = ImageFile(file=open(image_path, mode='rb'))
        new_image = compress_image_file(image=original_image)
        self.assertLess(new_image.size, original_image.size)
