from rest_framework import serializers
from apps.meme_wars.models import War
from apps.meme_wars.serializers import VotingScoreSerializer


class OngoingWarSerializer(serializers.ModelSerializer):
    voting_scores = VotingScoreSerializer(many=True)

    class Meta:
        model = War
        fields = ['id', 'name', 'has_ended', 'voting_scores', ]
