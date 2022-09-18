from rest_framework import serializers


class AbstractMemeSerializer(serializers.ModelSerializer):

    def __init__(self, request, **kwargs):
        super(AbstractMemeSerializer, self).__init__(**kwargs)
        self.request = request

    def to_representation(self, instance):
        data = super(AbstractMemeSerializer, self).to_representation(instance)
        data['image'] = self.request.build_absolute_uri(instance.image.url)
        return data
