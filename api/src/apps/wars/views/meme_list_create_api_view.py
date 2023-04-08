from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from apps.users.authentication import TokenAuthentication
from apps.wars.models import Meme
from apps.wars.serializers import MemeSerializer, CreateMemeSerializer


class MemeListCreateAPIView(ListCreateAPIView):
    queryset = Meme.objects.order_by('-created').all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_fields = ['war', 'approval_status']

    def get_serializer_class(self) -> type[MemeSerializer | CreateMemeSerializer]:
        return CreateMemeSerializer if self.request.method == 'POST' else MemeSerializer
