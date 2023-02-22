from http.client import NOT_FOUND
from typing import Type
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets
from apps.common.models import BaseModel
from apps.common.paginator import Paginator
from apps.common.serializers import ModelSerializer


class ViewSet(viewsets.ViewSet):
    current_handler: str
    model_class: Type[BaseModel]
    serializer_class: Type[ModelSerializer]
    available_alphabet_letters_default_field: str = None

    def retrieve(self, request, pk=None) -> JsonResponse:
        if instance := self.model_class.objects.filter(pk=pk).first():
            serializer_kwargs = self.get_serializer_kwargs(instance=instance)
            serializer = self.serializer_class(**serializer_kwargs)
            return JsonResponse(data=serializer.data)
        return JsonResponse(data={'message': _('Not fount')}, status=NOT_FOUND)

    def list(self, request) -> JsonResponse:
        queryset = self.model_class.objects.order_by('-created').all()
        paginator = Paginator(queryset=queryset, request=request)
        serializer_kwargs = self.get_serializer_kwargs(paginator=paginator)
        serializer = self.serializer_class(**serializer_kwargs)
        return JsonResponse(data=serializer.data, safe=False)

    def get_serializer_kwargs(self, **kwargs) -> dict:
        kwargs['request'] = self.request
        return kwargs
