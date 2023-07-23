from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.authentication import TokenAuthentication
from meme_wars.serializers import MessageSerializer


class LogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    response_data = {"message": _("Success")}

    @extend_schema(
        description=_("Logs out the authenticated user"),
        responses=MessageSerializer,
        examples=[
            OpenApiExample(
                name=_("Response"),
                value=response_data,
                request_only=False,
                response_only=True,
            ),
        ],
    )
    def get(self, *args, **kwargs) -> Response:
        self.request.user.auth_token.delete()
        return Response(data=self.response_data, status=200)
