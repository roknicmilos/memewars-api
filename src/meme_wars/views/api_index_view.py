from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from meme_wars.utils import build_absolute_api_uri


class APIIndexView(APIView):
    @extend_schema(
        description=_('Index endpoint for Meme Wars API'),
    )
    def get(self, *args, **kwargs) -> Response:
        data = {
            'urls': {
                'download_schema': build_absolute_api_uri("schema:download"),
                'swagger_ui': build_absolute_api_uri("schema:swagger"),
                'redoc_ui': build_absolute_api_uri("schema:redoc"),
            }
        }
        return Response(data=data)
