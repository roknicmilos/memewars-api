from django.conf import settings
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers

from apps.wars.models import Meme


@extend_schema_serializer(
    exclude_fields=('user',),
    examples=[
        OpenApiExample(
            name=_('Success response example'),
            summary=_('Created meme response'),
            description=_('A response example of successfully created meme'),
            value={
                'war': 1,
                'user': 1,
                'image': f'{settings.HOST_URL}{settings.MEDIA_URL}{Meme.image.field.upload_to.base_path}my-meme.jpg',
            },
            request_only=False,
            response_only=True,
        ),
    ]
)
class CreateMemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meme
        fields = ('war', 'user', 'image',)
