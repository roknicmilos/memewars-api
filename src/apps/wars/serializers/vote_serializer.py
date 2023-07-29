from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiExample, extend_schema_serializer

from apps.common.serializers import ModelWithUserSerializer
from apps.wars.models import Vote


@extend_schema_serializer(
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
class VoteSerializer(ModelWithUserSerializer):
    class Meta:
        model = Vote
        fields = "__all__"
        read_only_fields = ["submission_count"]
        ordering = ["created"]
