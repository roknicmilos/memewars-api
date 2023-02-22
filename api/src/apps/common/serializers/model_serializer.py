from rest_framework import serializers
from rest_framework.serializers import LIST_SERIALIZER_KWARGS

from apps.common.serializers import ListModelSerializer


class ModelSerializer(serializers.ModelSerializer):
    def __new__(cls, *args, **kwargs):
        if 'paginator' in kwargs:
            return cls.init_list_serializer(*args, **kwargs)
        return super().__new__(cls, *args, **kwargs)

    @classmethod
    def init_list_serializer(cls, *args, **kwargs):  # pragma: no cover
        """
        Implementation of this function is copied form
        rest_framework.serializers.BaseSerializer.many_init
        to override list model serializer class when "paginator"
        is passed to this class when instantiating it.
        """

        allow_empty = kwargs.pop('allow_empty', None)
        max_length = kwargs.pop('max_length', None)
        min_length = kwargs.pop('min_length', None)
        paginator = kwargs.pop('paginator')
        kwargs['instance'] = paginator.page
        nested_serializer = cls(*args, **kwargs)
        list_kwargs = {
            'child': nested_serializer,
            'total_items': paginator.total_items,
            'total_pages': paginator.total_pages,
            'request': kwargs.get('request'),
        }
        if allow_empty is not None:
            list_kwargs['allow_empty'] = allow_empty
        if max_length is not None:
            list_kwargs['max_length'] = max_length
        if min_length is not None:
            list_kwargs['min_length'] = min_length
        list_kwargs.update({key: value for key, value in kwargs.items() if key in LIST_SERIALIZER_KWARGS})
        return ListModelSerializer(*args, **list_kwargs)

    def __init__(self, request=None, **kwargs):
        super(ModelSerializer, self).__init__(**kwargs)
        self.request = request
