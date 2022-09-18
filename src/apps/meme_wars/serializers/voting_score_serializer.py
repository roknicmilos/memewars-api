from rest_framework import serializers
from apps.meme_wars.models import VotingScore


class VotingScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = VotingScore
        fields = ['id', 'order', 'label']
