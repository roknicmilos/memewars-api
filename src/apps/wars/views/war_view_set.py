from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from apps.users.authentication import TokenAuthentication


class WarViewSet(ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
