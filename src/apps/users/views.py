import json
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.authtoken.models import Token
from apps.users.models import User


@api_view(['POST'])
@renderer_classes([JSONRenderer])
def get_auth_toke(request) -> Response:
    data = json.loads(request.body)

    # TODO: validate data

    user = User.objects.filter(email=data.get('email')).first()
    if not (user and user.check_password(raw_password=data.get('password'))):
        return Response(status=400, data={'message': _('Invalid credentials')})

    token, __ = Token.objects.get_or_create(user=user)

    return Response(status=200, data={'token': token.key})
