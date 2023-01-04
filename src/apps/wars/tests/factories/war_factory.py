from factory.django import DjangoModelFactory

from apps.wars.models import War


class WarFactory(DjangoModelFactory):
    class Meta:
        model = War
