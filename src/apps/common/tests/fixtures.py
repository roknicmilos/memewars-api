from os.path import join

from django.conf import settings
from django.core.files.images import ImageFile


def get_image_file_example() -> ImageFile:
    image_path = join(settings.MEDIA_ROOT, "fixtures", "memes", "meme_template_1.jpg")
    return ImageFile(file=open(image_path, mode="rb"))
