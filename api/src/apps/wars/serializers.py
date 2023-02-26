from rest_framework import serializers

from apps.common.serializers import ModelSerializer
from apps.wars.models import War


class WarSerializer(ModelSerializer):
    voter_count = serializers.ReadOnlyField()
    meme_count = serializers.ReadOnlyField()

    class Meta:
        model = War
        fields = '__all__'
