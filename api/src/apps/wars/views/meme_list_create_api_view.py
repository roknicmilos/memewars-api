from django.utils.translation import gettext_lazy as _
from django.db.models import QuerySet, Q
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from apps.users.authentication import TokenAuthentication
from apps.wars.models import Meme, War
from apps.wars.serializers import MemeSerializer, CreateMemeSerializer


@extend_schema_view(
    get=extend_schema(
        description=_(
            'Memes are automatically filtered by their war phase and '
            'approval status (if their war requires approval status)'
        ),
        responses=MemeSerializer,
    ),
    post=extend_schema(
        description=_(
            'Memes can ony be created by and for authenticated users'
        ),
        request=CreateMemeSerializer,
        responses=CreateMemeSerializer,
    ),
)
class MemeListCreateAPIView(ListCreateAPIView):
    queryset = Meme.objects.order_by('-created').all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_fields = ['war', ]

    def get_serializer_class(self) -> type[MemeSerializer | CreateMemeSerializer]:
        return CreateMemeSerializer if self.request.method == 'POST' else MemeSerializer

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
        return Meme.objects.exclude(excludes).filter(filters).order_by('-created').all()

    def get_serializer(self, *args, **kwargs) -> CreateMemeSerializer | MemeSerializer:
        if self.request.method == 'POST':
            kwargs['data'] = {**kwargs['data'].dict(), 'user': self.request.user.pk}
            return super().get_serializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)
