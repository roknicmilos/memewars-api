from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.users.serializers import GoogleAuthLoginQuerySerializer


class GoogleAuthLoginURLAPIView(APIView):
    @extend_schema(
        description=_("Redirects the user to a Google login URL"),
        parameters=[GoogleAuthLoginQuerySerializer],
        responses={
            302: OpenApiResponse(description=_("Redirects the user to a Google login URL")),
            # TODO: add 400 response?
        },
    )
    def get(self, *args, **kwargs) -> HttpResponseRedirect | Response:
        serializer = GoogleAuthLoginQuerySerializer(request=self.request)
        serializer.is_valid(raise_exception=True)
        return redirect(to=serializer.login_url)
