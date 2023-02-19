from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from rest_framework.views import APIView

from apps.users.authentication import google_auth


class GoogleAuthLoginUrlAPIView(APIView):

    def get(self, *args, **kwargs) -> HttpResponseRedirect:
        google_login_url = google_auth.get_login_url(request=self.request)
        return redirect(to=google_login_url)
