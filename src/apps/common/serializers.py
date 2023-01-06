from rest_framework import serializers


class SimpleSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        pass  # pragma: no cover

    def create(self, validated_data):
        pass  # pragma: no cover
