from django.db.models import Avg, Q, QuerySet
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.users.authentication import TokenAuthentication
from apps.wars.models import Meme, War
from apps.wars.serializers import MemeSerializer


@extend_schema_view(
    get=extend_schema(
        description=_(
            "Memes are automatically filtered by their war phase and "
            "approval status (if their war requires approval status)"
        ),
        responses=MemeSerializer,
    ),
    post=extend_schema(
        description=_("Memes can ony be created by and for authenticated users"),
        request=MemeSerializer,
        responses=MemeSerializer,
    ),
)
class MemeListCreateAPIView(ListCreateAPIView):
    queryset = Meme.objects.order_by("-created").all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_fields = [
        "war",
    ]
    serializer_class = MemeSerializer

    def get_queryset(self) -> QuerySet:
        excludes = Q(war__phase=War.Phases.PREPARATION)
        filters = Q(
            # Filter memes that are approved
            Q(approval_status=Meme.ApprovalStatuses.APPROVED.value)
            # OR that belong to wars that do not require meme approval
            | Q(war__requires_meme_approval=False)
            # OR that belong to wars in the submission phase
            | Q(war__phase=War.Phases.SUBMISSION.value)
        )
        # Additionally,
        filters &= Q(
            # filter memes that belong to wars in VOTING or FINISHED phase
            Q(war__phase__in=[War.Phases.VOTING.value, War.Phases.FINISHED.value])
            # OR that belong to the authenticated user
            | Q(user=self.request.user)
        )

        queryset = Meme.objects.exclude(excludes).filter(filters)

        if self._should_order_by_score():
            return queryset.annotate(score=Avg("votes__score")).order_by("-score", "-created")

        return queryset.order_by("-created")

    def _should_order_by_score(self) -> bool:
        if war := War.objects.filter(pk=self.request.GET.get("war")).first():
            return war.phase == War.Phases.FINISHED
        return False
