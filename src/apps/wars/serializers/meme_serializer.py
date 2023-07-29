from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers

from apps.common.fields import ImageField
from apps.common.serializers import ModelWithUserSerializer
from apps.wars.models import Meme


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            name=_("Success response example"),
            summary=_("Created meme response"),
            description=_("A response example of successfully created meme"),
            value={
                "id": 1,
                "total_score": 0,
                "vote_count": 0,
                "war": 1,
                "user": 1,
                "image": f"{settings.HOST_URL}{settings.MEDIA_URL}{Meme.image.field.upload_to.base_path}my-meme.jpg",
                "created": now().isoformat(),
                "modified": now().isoformat(),
                "approval_status": Meme.ApprovalStatuses.PENDING.value,
            },
            request_only=False,
            response_only=True,
        ),
    ],
)
class MemeSerializer(ModelWithUserSerializer):
    total_score = serializers.ReadOnlyField()
    vote_count = serializers.ReadOnlyField()

    class Meta:
        model = Meme
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serializer_field_mapping[models.ImageField] = ImageField
