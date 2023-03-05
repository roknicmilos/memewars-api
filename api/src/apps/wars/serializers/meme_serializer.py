from django.db import models
from rest_framework import serializers

from apps.common.fields import ImageField
from apps.wars.models import Meme


class MemeSerializer(serializers.ModelSerializer):
    total_score = serializers.ReadOnlyField()
    vote_count = serializers.ReadOnlyField()

    class Meta:
        model = Meme
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serializer_field_mapping[models.ImageField] = ImageField
