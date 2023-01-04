import os
from typing import Type
from django.db.models import Model, TextChoices
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields.files import ImageFieldFile
from django.urls import reverse, NoReverseMatch
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from io import BytesIO
from PIL import Image, ImageOps
from django.core.files import File


def get_model_admin_change_details_url(obj: Model) -> str:
    content_type = ContentType.objects.get_for_model(obj.__class__)
    try:
        return reverse(f'admin:{content_type.app_label}_{content_type.model}_change', args=(obj.id,))
    except NoReverseMatch:
        return ''


@deconstructible
class FilePath:
    def __init__(self, base_path: str):
        self.base_path = base_path

    def __call__(self, instance, filename):
        filename_without_extension, file_extension = os.path.splitext(filename)
        timestamp_str = str(timezone.now().timestamp()).replace('.', '_')
        new_filename = f"{filename_without_extension}_{timestamp_str}{file_extension}"
        return os.path.join(self.base_path, new_filename)


def get_text_choice_by_value(value: str, text_choices: Type[TextChoices]) -> TextChoices:
    if value not in text_choices:
        raise ValueError(f'Value "{value}" is not {text_choices}')

    for choice in text_choices:
        if choice.value == value:
            return choice


def compress_image_file(image: ImageFieldFile, image_format: str = 'JPEG') -> File:
    prepared_image = Image.open(image)
    prepared_image = prepared_image.convert('RGB')  # Converts Image to RGB color mode
    prepared_image = ImageOps.exif_transpose(prepared_image)  # Auto rotates image according to EXIF data
    image_io = BytesIO()
    prepared_image.save(image_io, format=image_format, quality=80)
    return File(file=image_io, name=image.name)
