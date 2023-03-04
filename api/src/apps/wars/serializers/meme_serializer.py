from rest_framework import serializers

from apps.wars.models import Meme


class MemeSerializer(serializers.ModelSerializer):
    total_score = serializers.ReadOnlyField()
    vote_count = serializers.ReadOnlyField()

    class Meta:
        model = Meme
        fields = '__all__'
