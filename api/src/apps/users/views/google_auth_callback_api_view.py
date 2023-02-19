from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from apps.users.authentication import google_auth
from apps.users.utils import get_or_create_user


class GoogleAuthCallbackAPIView(APIView):

    def get(self, *args, **kwargs) -> HttpResponseRedirect:
        try:
            google_user = google_auth.get_user(request=self.request)
        except Exception:
            return redirect(to=google_auth.build_login_failure_url())

        user, _ = get_or_create_user(google_user=google_user)
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        login_success_url = google_auth.build_login_success_url(token=token)
        return redirect(to=login_success_url)
