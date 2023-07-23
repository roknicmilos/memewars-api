from django.contrib.auth import get_user_model

from apps.common.models import BaseModel, OriginalModelInstance
from meme_wars.tests.test_case import TestCase


class TestBaseModel(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.user_class = get_user_model()
        self.assertTrue(issubclass(self.user_class, BaseModel))
        self.user = self.user_class.objects.create()

    def test_should_set_attribute_original_when_accessing_it_for_the_first_time(self):
        self.assertIsInstance(self.user.original, OriginalModelInstance)

    def test_should_set_attribute_original_to_none_after_refresh_from_db(self):
        self.user._original = OriginalModelInstance(model_class=self.user_class, obj_id=self.user.pk)
        self.user.refresh_from_db()
        self.assertIsNone(self.user._original)
