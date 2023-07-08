from django.http import QueryDict
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from apps.users.authentication import TokenAuthentication
from apps.wars.models import Vote, War
from apps.wars.serializers import VoteSerializer


@extend_schema_view(
    post=extend_schema(
        description=_(
            'Votes can only be created by authenticated users '
            'and for memes in wars that are in the "voting" phase'
        ),
        request=VoteSerializer,
        responses=VoteSerializer,
    ),
)
class VoteCreateAPIView(CreateAPIView):
    queryset = Vote.objects.filter()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = VoteSerializer

    # TODO: extract into mixin class
    def get_serializer(self, *args, **kwargs) -> VoteSerializer:
        if self.request.method == 'POST':
            data = kwargs['data'].dict() if isinstance(kwargs['data'], QueryDict) else kwargs['data']
            kwargs['data'] = {**data, 'user': self.request.user.pk}
            return super().get_serializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)
