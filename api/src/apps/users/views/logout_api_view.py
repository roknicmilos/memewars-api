from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.authentication import TokenAuthentication


class LogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs) -> Response:
        self.request.user.auth_token.delete()
        return Response(data={'message': 'Success'}, status=200)
