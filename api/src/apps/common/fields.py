import os

from rest_framework.fields import ImageField as BaseImageField
from rest_framework.settings import api_settings

from urllib.parse import urlparse


class ImageField(BaseImageField):

    def to_representation(self, value) -> str:
        value = super().to_representation(value=value)
        if value and getattr(self, 'use_url', api_settings.UPLOADED_FILES_USE_URL):
            parsed_url = urlparse(url=value)
            return f"{os.getenv('WEB_API_BASE_URL')}{parsed_url.path}"
        return value
