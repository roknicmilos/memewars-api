from rest_framework import serializers
from apps.meme_wars.models import Vote


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'meme_id', 'user_id', 'score_id']

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
