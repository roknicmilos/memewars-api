import os
from typing import Type

from django.conf import settings
from django.core.files.images import ImageFile
from django.db.models import Model, TextChoices
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.urls import reverse, NoReverseMatch
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from io import BytesIO
from PIL import Image, ImageOps
from django.core.files import File
from rest_framework.exceptions import NotAuthenticated, AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import exception_handler

from apps.common.responses import ErrorResponse


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


def compress_image_file(image: ImageFile, image_format: str = 'JPEG') -> File:
    prepared_image = Image.open(image)
    prepared_image = prepared_image.convert('RGB')  # Converts Image to RGB color mode
    prepared_image = ImageOps.exif_transpose(prepared_image)  # Auto rotates image according to EXIF data
    image_io = BytesIO()
    quality = get_reduced_file_quality_percentage(file_size=image.size)
    prepared_image.save(image_io, format=image_format, quality=-1 if quality == 100 else quality)
    return File(file=image_io, name=image.name)


def get_reduced_file_quality_percentage(file_size: int) -> int:
    if file_size < 100000:
        return 100
    if file_size < 300000:
        return 80
    if file_size < 600000:
        return 70
    if file_size < 1000000:
        return 60
    return 50


def build_absolute_uri(view_name: str, args: tuple = None, kwargs: dict = None) -> str:
    return f'{settings.HOST_URL}{reverse(viewname=view_name, args=args, kwargs=kwargs)}'


def handle_api_exception(error: Exception, context: dict = None) -> Response:
    if isinstance(error, NotAuthenticated):
        return ErrorResponse(message='Authentication token was not provided', status=401)
    if isinstance(error, AuthenticationFailed):
        return ErrorResponse(message='Authentication token is invalid', status=401)
    if isinstance(error, Http404):
        return ErrorResponse(message='Not found', status=404)
    return exception_handler(exc=error, context=context)
