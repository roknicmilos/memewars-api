from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from apps.users.authentication import TokenAuthentication
from apps.wars.models import Meme
from apps.wars.serializers import MemeSerializer


class MemeListAPIView(ListAPIView):
    queryset = Meme.objects.order_by('-created').all()
    serializer_class = MemeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
