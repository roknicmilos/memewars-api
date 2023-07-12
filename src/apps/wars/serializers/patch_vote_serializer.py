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
            summary=_("Partial vote update response"),
            description=_("A response example of successful partial vote update"),
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
class PatchVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = [
            "score",
        ]

    def update(self, instance: Vote, validated_data: dict) -> Vote:
        validated_data["submission_count"] = instance.submission_count + 1
        return super().update(instance=instance, validated_data=validated_data)
