from unittest.mock import Mock

from django.conf import settings

from apps.common.fields import ImageField
from meme_wars.tests.test_case import TestCase


class TestImageField(TestCase):
    def test_should_return_image_url(self):
        image_field = ImageField()
        mock_value = Mock()
        mock_value.url = "/mocked/url/path"
        image_url = image_field.to_representation(value=mock_value)
        self.assertEqual(image_url, f"{settings.HOST_URL}{mock_value.url}")

    def test_should_return_image_name(self):
        image_field = ImageField(use_url=False)
        mock_value = Mock()
        mock_value.name = "mocked-name"
        image_name = image_field.to_representation(value=mock_value)
        self.assertEqual(image_name, mock_value.name)
