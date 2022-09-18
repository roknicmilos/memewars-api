from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.users.models import User
from apps.meme_wars.models import Vote, Meme, VotingScore


class SubmitVoteSerializer(serializers.Serializer):
    meme_id = serializers.IntegerField()
    score_id = serializers.IntegerField(required=False)

    def __init__(self, user: User, *args, **kwargs):
        super(SubmitVoteSerializer, self).__init__(*args, **kwargs)
        self.user = user
        self.meme = None
        self.score = None
        self.vote = None

    def validate_meme_id(self, meme_id: int) -> None:
        try:
            self.meme = Meme.objects.get(pk=meme_id)
        except Meme.DoesNotExist:
            raise ValidationError(_('Meme not found'))

    def validate_score_id(self, score_id: int) -> None:
        if score_id and self.meme:
            try:
                self.score = self.meme.war.voting_scores.get(pk=score_id)
            except VotingScore.DoesNotExist:
                raise ValidationError(_('Voting score not found'))

    def validate(self, data):
        try:
            self.vote = Vote.objects.get(user=self.user, meme=self.meme)
        except Vote.DoesNotExist:
            self.vote = Vote(user=self.user, meme=self.meme)

        if self.score:
            self.vote.score = self.score

        if self.vote.pk:
            self.vote.submission_count += 1

        self.vote.full_clean()

        return super(SubmitVoteSerializer, self).validate(data)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
