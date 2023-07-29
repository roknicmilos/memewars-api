from django.contrib.auth import get_user_model
from django.core.handlers.wsgi import WSGIRequest
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
    user_model = get_user_model()

    def __new__(cls, *args, **kwargs):
        meta = getattr(cls, "Meta", object)

        user_field = getattr(meta.model, cls.user_field_name, None)
        if (
            not user_field
            or not isinstance(user_field.field, models.ForeignKey)
            or user_field.field.target_field.model != cls.user_model
        ):
            raise AttributeError(
                f"Model class must have 'user' ForeignKey field with "
                f"'{cls.user_model.__module__}.{cls.user_model.__name__}' remote model"
            )

        # TODO: TEST
        #   1. when read_only_fields is not define in serializer Meta class
        #   2. when read_only_fields is define in serializer Meta class, but it doesn't have "user"
        #   3. when read_only_fields is define in serializer Meta class and it has "user" (check no duplicates)
        read_only_fields = getattr(meta, "read_only_fields", ())
        if cls.user_field_name not in read_only_fields:
            read_only_fields += (cls.user_field_name,)
        setattr(meta, "read_only_fields", read_only_fields)

        return super().__new__(cls, *args, **kwargs)

    def __init__(self, request: WSGIRequest, instance=None, data=empty, **kwargs):
        if not isinstance(request.user, self.user_model):
            # TODO: TEST
            #   1. when user is not authenticated
            #   2. when user is authenticated
            raise PermissionError("Authenticated user is required")
        self.user = request.user
        super().__init__(instance, data, **kwargs)

    def save(self, **kwargs) -> BaseModel:
        # TODO: TEST model is saved with the self.user
        kwargs[self.user_field_name] = self.user
        return super().save(**kwargs)
