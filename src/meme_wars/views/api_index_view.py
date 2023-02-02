from rest_framework.response import Response
from rest_framework.views import APIView


class APIIndexView(APIView):

    @staticmethod
    def get(*args, **kwargs):
        return Response(data='This is the base URL for the Meme Wars API')
