from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from apps.users.utils import get_or_create_user, build_login_failure_url, build_login_success_url


class GoogleAuthCallbackAPIView(APIView):

    def get(self, *args, **kwargs) -> HttpResponseRedirect:
        try:
            user, _ = get_or_create_user(request=self.request)
        except Exception as error:
            return redirect(to=build_login_failure_url(error=error))
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        return redirect(to=build_login_success_url(token=token))
