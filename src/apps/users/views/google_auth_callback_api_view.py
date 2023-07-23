from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from apps.users.serializers import GoogleAuthCallbackQuerySerializer


class GoogleAuthCallbackAPIView(APIView):
    @extend_schema(
        description=_("The endpoint for a request from Google sent after successful Google login"),
        parameters=[GoogleAuthCallbackQuerySerializer],
        responses={
            302: OpenApiResponse(description=_("Redirects the user to the the login success or the login failure URL"))
        },
    )
    def get(self, *args, **kwargs) -> HttpResponseRedirect:
        serializer = GoogleAuthCallbackQuerySerializer(request=self.request)
        if not serializer.is_valid():
            return redirect(to=serializer.build_login_failure_url())

        user, _ = serializer.get_or_create_user()
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        return redirect(to=serializer.build_login_success_url(token=token))
