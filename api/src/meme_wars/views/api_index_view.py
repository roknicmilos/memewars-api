from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework.response import Response
from rest_framework.views import APIView

from meme_wars.serializers import MessageSerializer


class APIIndexView(APIView):
    response_data = {'message': _('This is the base URL for the Meme Wars API')}

    @extend_schema(
        responses=MessageSerializer,
        examples=[
            OpenApiExample(
                name=_('Response'),
                value=response_data,
                request_only=False,
                response_only=True,
            ),
        ]
    )
    def get(self, *args, **kwargs) -> Response:
        return Response(data=self.response_data)
