from typing import Type

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from rest_framework import viewsets
from apps.common.models import BaseModel
from apps.common.paginator import Paginator
from apps.common.serializers import ModelSerializer


class ViewSet(viewsets.ViewSet):
    model_class: Type[BaseModel]
    serializer_class: Type[ModelSerializer]

    def list(self, request: WSGIRequest) -> JsonResponse:
        queryset = self.model_class.objects.order_by('-created').all()
        paginator = Paginator(queryset=queryset, request=request)
        serializer_kwargs = self.get_serializer_kwargs(paginator=paginator)
        serializer = self.serializer_class(**serializer_kwargs)
        return JsonResponse(data=serializer.data, safe=False)

    def get_serializer_kwargs(self, **kwargs) -> dict:
        kwargs['request'] = self.request
        return kwargs

