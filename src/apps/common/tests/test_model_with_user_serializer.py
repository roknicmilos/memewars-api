from unittest.mock import patch

import pytest
from django.contrib.auth.models import AnonymousUser
from django.db import models

from apps.common import serializers as common_serializers
from apps.common.models import BaseModel
from meme_wars.tests.test_case import TestCase

"""
Models defined in this file will be migrated to the temporary
tests database(s) even though they have no migration files.

Model migrations will FAIL if the app has migrations (module
"migrations").
"""


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


class FakeUserModel(BaseModel):
    class Meta:
        app_label = "common"


class ModelWithUserExampleC(BaseModel):
    """
    A model that has "user" ForeignKey field, but
    it doesn't have User remote model
    """

    user = models.ForeignKey(
        to=FakeUserModel,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        app_label = "common"


class TestModelWithUserSerializer(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.get_user_model_patcher = patch.object(
            target=common_serializers, attribute="get_user_model", return_value=FakeUserModel
        )
        self.get_user_model_patcher.start()

    def test_should_raise_attribute_error(self):
        """
        When a model used in a serializer class that inherits from
        ModelWithUserSerializer doesn't have "user" ForeignKey field
        with correct User model as the target model, __new__ method
        of that serializer class should raise the AttributeError.
        """

        expected_error_message = (
            f"Model class must have 'user' ForeignKey field with "
            f"'{FakeUserModel.__module__}.{FakeUserModel.__name__}' remote model"
        )

        # When a serializer has a model class without "user" field
        class ModelWithoutUserExampleSerializer(common_serializers.ModelWithUserSerializer):
            class Meta:
                model = ModelWithoutUserExample

        with pytest.raises(AttributeError, match=expected_error_message):
            ModelWithoutUserExampleSerializer.__new__(ModelWithoutUserExampleSerializer)

        # When a serializer has a model class with "user" field that is not ForeignKey
        class ModelWithUserExampleASerializer(common_serializers.ModelWithUserSerializer):
            class Meta:
                model = ModelWithUserExampleA

        with pytest.raises(AttributeError, match=expected_error_message):
            ModelWithUserExampleASerializer.__new__(ModelWithUserExampleASerializer)

        # When a serializer has a model class with ForeignKey "user" field that has
        # incorrect remote model (not the User model)
        class ModelWithUserExampleBSerializer(common_serializers.ModelWithUserSerializer):
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

        class ModelWithUserExampleCSerializer(common_serializers.ModelWithUserSerializer):
            class Meta:
                model = ModelWithUserExampleC

        ModelWithUserExampleCSerializer.__new__(ModelWithUserExampleCSerializer)

    def test_should_add_user_to_read_only_fields(self):
        # When read_only_fields is not define in serializer Meta class:
        class SerializerWithoutReadOnlyFields(common_serializers.ModelWithUserSerializer):
            class Meta:
                model = ModelWithUserExampleC

        SerializerWithoutReadOnlyFields.__new__(SerializerWithoutReadOnlyFields)
        meta = getattr(SerializerWithoutReadOnlyFields, "Meta")
        read_only_fields = getattr(meta, "read_only_fields")
        self.assertEqual(read_only_fields, ("user",))

        # When read_only_fields is define in serializer Meta class, but it doesn't have "user":
        class SerializerWithEmptyReadOnlyFields(common_serializers.ModelWithUserSerializer):
            class Meta:
                model = ModelWithUserExampleC
                read_only_fields = []

        SerializerWithEmptyReadOnlyFields.__new__(SerializerWithEmptyReadOnlyFields)
        meta = getattr(SerializerWithEmptyReadOnlyFields, "Meta")
        read_only_fields = getattr(meta, "read_only_fields")
        self.assertEqual(read_only_fields, ("user",))

    def test_should_not_add_user_to_read_only_fields(self):
        """
        When a serializer class already has "user" field in
        read_only_fields, the field should not be added to
        read_only_fields
        """

        class SerializerWithReadOnlyFields(common_serializers.ModelWithUserSerializer):
            class Meta:
                model = ModelWithUserExampleC
                read_only_fields = ["user", "id"]

        SerializerWithReadOnlyFields.__new__(SerializerWithReadOnlyFields)
        meta = getattr(SerializerWithReadOnlyFields, "Meta")
        read_only_fields = getattr(meta, "read_only_fields")
        self.assertEqual(read_only_fields, ("user", "id"))

    def test_should_raise_permission_error_when_authenticated_user_is_not_set(self):
        class Serializer(common_serializers.ModelWithUserSerializer):
            class Meta:
                model = ModelWithUserExampleC

        request = self.get_request_example()
        request.user = AnonymousUser()
        serializer = Serializer(context={"request": request})
        with pytest.raises(PermissionError, match="Authenticated user is required"):
            serializer.is_valid()

    def test_should_not_raise_permission_error_when_authenticated_user_is_set(self):
        class Serializer(common_serializers.ModelWithUserSerializer):
            class Meta:
                model = ModelWithUserExampleC
                fields = "__all__"

        request = self.get_request_example()
        request.user = FakeUserModel()
        serializer = Serializer(data={}, context={"request": request})
        serializer.is_valid()

    def test_should_save_model_instance_with_user_reference(self):
        class Serializer(common_serializers.ModelWithUserSerializer):
            class Meta:
                model = ModelWithUserExampleC
                fields = "__all__"

        request = self.get_request_example()
        request.user = FakeUserModel.objects.create()
        serializer = Serializer(data={}, context={"request": request})
        serializer.is_valid()
        instance = serializer.save()
        self.assertEqual(instance.user, request.user)

    def tearDown(self) -> None:
        super().tearDown()
        self.get_user_model_patcher.stop()
