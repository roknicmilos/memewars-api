from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from apps.users.authentication import TokenAuthentication
from apps.wars.models import War
from apps.wars.serializers import WarSerializer


class WarRetrieveAPIView(RetrieveAPIView):
    queryset = War.objects.all()
    serializer_class = WarSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
