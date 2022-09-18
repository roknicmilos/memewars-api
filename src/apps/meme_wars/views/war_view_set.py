from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from apps.users.authentication import TokenAuthentication
from apps.meme_wars.models import War
from apps.meme_wars.serializers import OngoingWarSerializer, EndedWarSerializer


class WarViewSet(ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk: int) -> Response:
        war = get_object_or_404(War, pk=pk, is_published=True)
        return Response(data=self._serialize_war(war=war))

    def list(self, request, **kwargs) -> Response:
        serialized_wars = [self._serialize_war(war=war) for war in War.objects.filter(is_published=True)]
        return Response(data=serialized_wars)

    def _serialize_war(self, war: War) -> dict:
        if war.has_ended:
            return EndedWarSerializer(request=self.request, instance=war).data
        return OngoingWarSerializer(instance=war).data
