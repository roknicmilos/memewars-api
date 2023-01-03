from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _
from apps.common.serializers import SimpleSerializer
from apps.users.models import User


class LoginSerializer(SimpleSerializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super(LoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        self.user = User.objects.filter(email=attrs['email']).first()
        if not (self.user and self.user.check_password(raw_password=attrs['password'])):
            raise serializers.ValidationError(_('Invalid credentials'))

        return attrs

    @property
    def validated_data(self):
        token, _ = Token.objects.get_or_create(user=self.user)
        return {'token': token.key}
