from apps.common.serializers import ModelSerializer
from apps.wars.models import Meme


class MemeSerializer(ModelSerializer):

    class Meta:
        model = Meme
        fields = '__all__'
