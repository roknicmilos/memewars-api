from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from apps.users.authentication import TokenAuthentication
from apps.meme_wars.models import Vote
from apps.meme_wars.serializers import SubmitVoteSerializer, VoteSerializer


class VoteViewSet(ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, *args, **kwargs) -> Response:
        votes = Vote.objects.filter(self._get_vote_filters())
        vote_serializer = VoteSerializer(instance=votes, many=True)
        return Response(data=vote_serializer.data)

    def _get_vote_filters(self) -> Q:
        filters = Q(meme__enlistment__war__is_published=True)

        war_id = self.request.GET.get('war_id')
        if war_id:
            filters &= Q(meme__enlistment__war=war_id)

        user_id = self.request.GET.get('user_id')
        if user_id:
            filters &= Q(user_id=self.request.user.id)

        return filters

    def create(self, *arg, **kwargs) -> Response:
        vote_serializer = SubmitVoteSerializer(data=self.request.data, user=self.request.user)
        if vote_serializer.is_valid():
            is_new_vote = not bool(vote_serializer.vote.pk)
            vote_serializer.vote.save()
            message = _('Vote has been created') if is_new_vote else _('Vote has been updated')
            return Response(status=201 if is_new_vote else 200, data={'message': message})

        return Response(status=400, data={'errors': vote_serializer.errors})
