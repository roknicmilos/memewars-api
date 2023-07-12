from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.users.authentication import TokenAuthentication
from apps.wars.models import War
from apps.wars.serializers import WarSerializer


class WarListAPIView(ListAPIView):
    queryset = War.objects.order_by("-created").all()
    serializer_class = WarSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
