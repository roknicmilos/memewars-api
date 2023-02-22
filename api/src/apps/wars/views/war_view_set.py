from rest_framework.permissions import IsAuthenticated

from apps.common.viewsets import ViewSet
from apps.users.authentication import TokenAuthentication
from apps.wars.models import War
from apps.wars.serializers import WarSerializer


class WarViewSet(ViewSet):
    model_class = War
    serializer_class = WarSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
