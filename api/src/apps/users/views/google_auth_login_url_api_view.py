from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.authentication import google_auth


class GoogleAuthLoginUrlAPIView(APIView):

    def get(self, *args, **kwargs) -> Response:
        google_login_url = google_auth.get_login_url(request=self.request)
        return Response(data={'url': google_login_url}, status=200)
