from typing import Type

from django.db.models import Model
from django.forms import model_to_dict


class OriginalModelInstance:
    def __init__(self, model_class: Type[Model], obj_id: int):
        self._set_kwargs(model_claas=model_class, obj_id=obj_id)
        for key, value in self.kwargs.items():
            setattr(self, key, value)

    def _set_kwargs(self, model_claas: Type[Model], obj_id: int) -> None:
        instance = model_claas.objects.get(pk=obj_id)
        self.kwargs = model_to_dict(instance)
        prop_names = [key for key, value in vars(instance.__class__).items() if type(value) is property]
        for prop_name in prop_names:
            self.kwargs[prop_name] = getattr(instance, prop_name)

    def dict(self) -> dict:
        return self.kwargs
