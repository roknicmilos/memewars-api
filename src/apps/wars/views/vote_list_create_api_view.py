from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.users.authentication import TokenAuthentication
from apps.wars.models import Vote
from apps.wars.serializers import VoteSerializer
from apps.wars.views.filters import VoteFilterSet


@extend_schema_view(
    post=extend_schema(
        description=_(
            'Votes can only be created by authenticated users and for memes in wars that are in the "voting" phase'
        ),
        request=VoteSerializer,
        responses=VoteSerializer,
    ),
)
class VoteListCreateAPIView(ListCreateAPIView):
    queryset = Vote.objects.all().order_by("-created")
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = VoteSerializer
    filterset_class = VoteFilterSet
