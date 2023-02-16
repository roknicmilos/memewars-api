from django.http import HttpResponseRedirect
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from apps.users.authentication import google_auth
from apps.users.utils import build_login_success_url, get_or_create_user, build_login_failure_url


class GoogleAuthCallbackAPIView(APIView):

    @staticmethod
    def get(request, **kwargs) -> HttpResponseRedirect:
        try:
            google_user = google_auth.get_user(request=request)
            user, is_created = get_or_create_user(google_user=google_user)
        except Exception:
            return HttpResponseRedirect(redirect_to=build_login_failure_url())

        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        login_success_url = build_login_success_url(token_key=token.key, is_new_user=is_created)
        return HttpResponseRedirect(redirect_to=login_success_url)
