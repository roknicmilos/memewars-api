from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from apps.users.serializers import GoogleAuthCallbackQuerySerializer
from apps.users.utils import build_login_failure_url, build_login_success_url


class GoogleAuthCallbackAPIView(APIView):

    @extend_schema(
        description=_('The endpoint for a request from Google sent after successful Google login'),
        parameters=[
            GoogleAuthCallbackQuerySerializer
        ],
        responses={
            302: OpenApiResponse(
                description=_('Redirects the user to the the login success or the login failure URL')
            )
        }
    )
    def get(self, *args, **kwargs) -> HttpResponseRedirect:
        serializer = GoogleAuthCallbackQuerySerializer(request=self.request)
        try:
            user, _ = serializer.get_or_create_user()
        except Exception as error:
            return redirect(to=build_login_failure_url(error=error))

        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        return redirect(to=build_login_success_url(token=token))
