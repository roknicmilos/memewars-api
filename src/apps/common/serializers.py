from django.contrib.auth import get_user_model
from django.db import models
from rest_framework import serializers
from rest_framework.fields import empty

from apps.common.models import BaseModel


class ModelWithUserSerializer(serializers.ModelSerializer):
    """
    Meant to be used by model serializers with models that have
    "user" ForeignKey field, where the value of that field should
    be the authenticated user.

    Requires a "request" object from which the authenticated
    User instance will be taken and added to the validated data.
    """

    user_field_name = "user"

    def __new__(cls, *args, **kwargs):
        user_model = get_user_model()
        meta = getattr(cls, "Meta", object)
        user_field = getattr(meta.model, cls.user_field_name, None)
        if (
            not user_field
            or not isinstance(user_field.field, models.ForeignKey)
            or user_field.field.target_field.model != user_model
        ):
            raise AttributeError(
                f"Model class must have 'user' ForeignKey field with "
                f"'{user_model.__module__}.{user_model.__name__}' "
                f"remote model"
            )

        read_only_fields = tuple(getattr(meta, "read_only_fields", ()))
        if cls.user_field_name not in read_only_fields:
            read_only_fields += (cls.user_field_name,)
        setattr(meta, "read_only_fields", read_only_fields)

        return super().__new__(cls, *args, **kwargs)

    def __init__(self, instance=None, data=empty, **kwargs):
        request = kwargs.get("context", {}).get("request")
        self.user = getattr(request, "user", None)
        super().__init__(instance, data, **kwargs)

    def is_valid(self, *, raise_exception=False) -> bool:
        if not isinstance(self.user, get_user_model()):
            raise PermissionError("Authenticated user is required")
        return super().is_valid(raise_exception=raise_exception)

    def save(self, **kwargs) -> BaseModel:
        kwargs[self.user_field_name] = self.user
        return super().save(**kwargs)
