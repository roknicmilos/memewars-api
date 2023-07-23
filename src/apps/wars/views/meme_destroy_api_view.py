from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.users.authentication import TokenAuthentication


@extend_schema_view(
    delete=extend_schema(
        description=_("Deletes a meme of the authenticated user"),
        responses={204: OpenApiResponse()},
    ),
)
class MemeDestroyAPIView(DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        return self.request.user.memes
