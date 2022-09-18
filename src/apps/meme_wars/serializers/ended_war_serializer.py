from rest_framework import serializers
from apps.meme_wars.models import Meme, War
from apps.meme_wars.serializers import AbstractMemeSerializer, VotingScoreSerializer


class EndedWarMemeSerializer(AbstractMemeSerializer):
    class Meta:
        model = Meme
        fields = ['id', 'image', 'vote_count', 'scored_value', ]

class WarMemesField(serializers.Field):

    def __init__(self, *args, **kwargs):
        super(WarMemesField, self).__init__(*args, **kwargs)
        self.request = None

    def to_representation(self, value):
        meme_serializer = EndedWarMemeSerializer(request=self.request, instance=value, many=True)
        return meme_serializer.data

    def to_internal_value(self, data):
        pass

class EndedWarSerializer(serializers.ModelSerializer):
    voting_scores = VotingScoreSerializer(many=True)
    memes = WarMemesField()

    class Meta:
        model = War
        fields = ['id', 'name', 'has_ended', 'voting_scores', 'memes']

    def __init__(self, request, **kwargs):
        super(EndedWarSerializer, self).__init__(**kwargs)
        self.required = request
        self.fields.fields['memes'].request = request

    def to_representation(self, value):
        war = super(EndedWarSerializer, self).to_representation(value)
        war['memes'].sort(key=lambda meme: meme.get('scored_value'), reverse=True)
        return war
