from unittest.mock import patch

import factory
from factory.django import DjangoModelFactory
from faker import Faker

from apps.users.tests.factories import UserFactory
from apps.wars.models import Meme
from apps.wars.models import meme as meme_model_file
from apps.wars.tests.factories import WarFactory

faker = Faker()


class MemeFactory(DjangoModelFactory):
    class Meta:
        model = Meme

    user = factory.LazyAttribute(lambda _: UserFactory())
    war = factory.LazyAttribute(lambda _: WarFactory())

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        if "image" not in kwargs:
            kwargs["image"] = faker.file_extension(category="image")
            with patch.object(meme_model_file, "compress_image_file") as mock_compress_image_file:
                mock_compress_image_file.return_value = kwargs["image"]
                return super()._create(model_class, *args, **kwargs)
        return super()._create(model_class, *args, **kwargs)
