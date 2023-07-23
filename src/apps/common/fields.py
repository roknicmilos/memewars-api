from urllib.parse import urlparse

from django.conf import settings
from rest_framework.fields import ImageField as BaseImageField
from rest_framework.settings import api_settings


class ImageField(BaseImageField):
    def to_representation(self, value) -> str:
        value = super().to_representation(value=value)
        if value and getattr(self, "use_url", api_settings.UPLOADED_FILES_USE_URL):
            parsed_url = urlparse(url=value)
            return f"{settings.HOST_URL}{parsed_url.path}"
        return value
