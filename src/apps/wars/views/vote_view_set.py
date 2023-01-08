from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from apps.users.authentication import TokenAuthentication


class VoteViewSet(ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, *args, **kwargs):
        return Response(data={'message': 'TMP Vote "list" endpoint response'})

    def retrieve(self, *args, **kwargs):
        return Response(data={'message': 'TMP Vote "retrieve" endpoint response'})
