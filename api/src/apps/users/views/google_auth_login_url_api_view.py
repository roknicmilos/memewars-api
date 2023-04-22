from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.views import APIView

from apps.users.authentication import google_auth


class GoogleAuthLoginUrlAPIView(APIView):

    @extend_schema(
        responses={
            302: OpenApiResponse(
                description=_('Redirects to a Google login URL')
            )
        }
    )
    def get(self, *args, **kwargs) -> HttpResponseRedirect:
        google_login_url = google_auth.get_login_url(request=self.request)
        return redirect(to=google_login_url)
