from rest_framework import serializers
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample

from apps.wars.models import Vote


@extend_schema_serializer(
    exclude_fields=("user",),
    examples=[
        OpenApiExample(
            name=_("Success response example"),
            summary=_("Created/updated vote response"),
            description=_("A response example of successfully created or updated vote"),
            value={
                "id": 1,
                "user": 1,
                "meme": 1,
                "score": 5,
                "submission_count": 1,
                "created": now().isoformat(),
                "modified": now().isoformat(),
            },
            request_only=False,
            response_only=True,
        ),
    ],
)
class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ["id", "score", "meme", "user", "submission_count", "created", "modified"]
        ordering = ["created"]
