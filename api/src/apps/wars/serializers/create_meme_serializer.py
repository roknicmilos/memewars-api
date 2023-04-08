from rest_framework import serializers

from apps.wars.models import Meme


class CreateMemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meme
        fields = ('war', 'user', 'image',)
