from apps.common.serializers import ModelSerializer
from apps.wars.models import War


class WarSerializer(ModelSerializer):
    class Meta:
        model = War
        fields = '__all__'
