from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.users.authentication import TokenAuthentication
from apps.wars.models import Vote
from apps.wars.serializers import PatchVoteSerializer


@extend_schema_view(
    patch=extend_schema(
        description=_("Votes can only be updated by the authenticated users that created those votes"),
        request=PatchVoteSerializer,
        responses=PatchVoteSerializer,
    ),
    put=extend_schema(exclude=True),
)
class VotePatchAPIView(UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PatchVoteSerializer

    def get_queryset(self) -> QuerySet:
        return Vote.objects.filter(user=self.request.user)
