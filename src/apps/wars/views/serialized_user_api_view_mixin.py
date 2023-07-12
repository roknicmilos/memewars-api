from django.http import QueryDict
from rest_framework.generics import GenericAPIView
from rest_framework.serializers import Serializer


class SerializedUserAPIViewMixin(GenericAPIView):
    def get_serializer(self, *args, **kwargs) -> Serializer:
        if self.request.method == "POST":
            data = kwargs["data"].dict() if isinstance(kwargs["data"], QueryDict) else kwargs["data"]
            kwargs["data"] = {**data, "user": self.request.user.pk}
        return super().get_serializer(*args, **kwargs)
