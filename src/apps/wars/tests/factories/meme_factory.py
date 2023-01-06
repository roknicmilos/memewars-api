from factory.django import DjangoModelFactory

from apps.users.tests.factories import UserFactory
from apps.wars.models import Meme
from apps.wars.tests.factories import WarFactory


class MemeFactory(DjangoModelFactory):
    class Meta:
        model = Meme

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        if 'user' not in kwargs:
            kwargs['user'] = UserFactory()
        if 'war' not in kwargs:
            kwargs['war'] = WarFactory()
        return super(MemeFactory, cls)._create(model_class, *args, **kwargs)
