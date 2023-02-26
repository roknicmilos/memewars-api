from rest_framework.permissions import IsAuthenticated

from apps.common.viewsets import ViewSet
from apps.users.authentication import TokenAuthentication
from apps.wars.models import Meme
from apps.wars.serializers import MemeSerializer


class MemeViewSet(ViewSet):
    model_class = Meme
    serializer_class = MemeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
