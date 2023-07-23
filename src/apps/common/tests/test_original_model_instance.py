from django.contrib.auth.models import Group

from apps.common.models import OriginalModelInstance
from meme_wars.tests.test_case import TestCase


class TestOriginalModelInstance(TestCase):
    def test_should_have_all_attributes_and_properties_as_the_original_object(self):
        @property
        def prop(_):
            return "prop value"

        Group.prop = prop
        group = Group.objects.create(name="New group")
        original_model_instance = OriginalModelInstance(model_class=Group, obj_id=group.pk)
        self.assertEqual(original_model_instance.id, group.id)
        self.assertEqual(original_model_instance.name, group.name)
        self.assertEqual(original_model_instance.prop, group.prop)
        self.assertEqual(original_model_instance.permissions, list(group.permissions.all()))

        expected_kwargs = {
            "id": group.id,
            "name": group.name,
            "permissions": list(group.permissions.all()),
            "prop": group.prop,
        }
        self.assertEqual(original_model_instance.kwargs, expected_kwargs)

        self.assertEqual(original_model_instance.dict(), expected_kwargs)
