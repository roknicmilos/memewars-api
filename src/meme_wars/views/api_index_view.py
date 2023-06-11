from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView


class APIIndexView(APIView):
    @extend_schema(
        description=_('Index endpoint for Meme Wars API'),
    )
    def get(self, *args, **kwargs) -> Response:
        base_url = self.request.build_absolute_uri()
        if base_url.endswith('/'):
            base_url = base_url[:-1]
        data = {
            'urls': {
                'download_schema': f'{base_url}{reverse("schema:download")}',
                'swagger_ui': f'{base_url}{reverse("schema:swagger")}',
                'redoc_ui': f'{base_url}{reverse("schema:redoc")}',
            }
        }
        return Response(data=data)
