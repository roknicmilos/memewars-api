import pytest
from django.contrib.auth import get_user_model
from django.db import models

from apps.common.models import BaseModel
from apps.common.serializers import ModelWithUserSerializer
from meme_wars.tests.test_case import TestCase

"""
Models defined in this file will be migrated to the temporary
tests database(s) even though they have no migration files.

Model migrations will FAIL if the app has migrations (module
"migrations").
"""

user_model = get_user_model()


class ModelWithoutUserExample(BaseModel):
    """
    A model that has no ForeignKey field with User
    remote model
    """

    class Meta:
        app_label = "common"


class ModelWithUserExampleA(BaseModel):
    """
    A model that has "user" field, but it is not
    ForeignKey
    """

    user = models.CharField(default="")

    class Meta:
        app_label = "common"


class ModelWithUserExampleB(BaseModel):
    """
    A model that has "user" ForeignKey field, but
    it doesn't have User remote model
    """

    user = models.ForeignKey(
        to=ModelWithUserExampleA,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        app_label = "common"


class ModelWithUserExampleC(BaseModel):
    """
    A model that has "user" ForeignKey field, but
    it doesn't have User remote model
    """

    user = models.ForeignKey(
        to=user_model,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        app_label = "common"


class TestModelWithUserSerializer(TestCase):
    def test_should_raise_attribute_error(self):
        """
        When a model used in a serializer class that inherits from
        ModelWithUserSerializer doesn't have "user" ForeignKey field
        with correct User model as the target model, __new__ method
        of that serializer class should raise the AttributeError.
        """

        expected_error_message = (
            f"Model class must have 'user' ForeignKey field with "
            f"'{user_model.__module__}.{user_model.__name__}' remote model"
        )

        # When a serializer has a model class without "user" field
        class ModelWithoutUserExampleSerializer(ModelWithUserSerializer):
            class Meta:
                model = ModelWithoutUserExample

        with pytest.raises(AttributeError, match=expected_error_message):
            ModelWithoutUserExampleSerializer.__new__(ModelWithoutUserExampleSerializer)

        # When a serializer has a model class with "user" field that is not ForeignKey
        class ModelWithUserExampleASerializer(ModelWithUserSerializer):
            class Meta:
                model = ModelWithUserExampleA

        with pytest.raises(AttributeError, match=expected_error_message):
            ModelWithUserExampleASerializer.__new__(ModelWithUserExampleASerializer)

        # When a serializer has a model class with ForeignKey "user" field that has
        # incorrect remote model (not the User model)
        class ModelWithUserExampleBSerializer(ModelWithUserSerializer):
            class Meta:
                model = ModelWithUserExampleB

        with pytest.raises(AttributeError, match=expected_error_message):
            ModelWithUserExampleBSerializer.__new__(ModelWithUserExampleBSerializer)

    def test_should_not_raise_attribute_error(self):
        """
        When a model used in a serializer class that inherits from
        ModelWithUserSerializer has "user" ForeignKey field with
        correct User model as the target model, __new__ method of
        that serializer class should not raise the AttributeError.
        """

        class ModelWithUserExampleCSerializer(ModelWithUserSerializer):
            class Meta:
                model = ModelWithUserExampleC

        ModelWithUserExampleCSerializer.__new__(ModelWithUserExampleCSerializer)
