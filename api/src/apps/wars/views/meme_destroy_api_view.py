from django.db.models import QuerySet
from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.users.authentication import TokenAuthentication


class MemeDestroyAPIView(DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        return self.request.user.memes
