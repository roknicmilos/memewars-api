from apps.meme_wars.models import Meme
from apps.meme_wars.serializers import AbstractMemeSerializer


class OngoingWarMemeSerializer(AbstractMemeSerializer):
    class Meta:
        model = Meme
        fields = ['id', 'image', ]
