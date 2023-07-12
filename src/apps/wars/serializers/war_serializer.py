from rest_framework import serializers

from apps.wars.models import War


class WarSerializer(serializers.ModelSerializer):
    voter_count = serializers.ReadOnlyField()
    meme_count = serializers.ReadOnlyField()

    class Meta:
        model = War
        fields = "__all__"
