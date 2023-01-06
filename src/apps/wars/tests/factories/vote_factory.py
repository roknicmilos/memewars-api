from random import randint

from factory.django import DjangoModelFactory

from apps.users.tests.factories import UserFactory
from apps.wars.models import Vote
from apps.wars.tests.factories import MemeFactory


class VoteFactory(DjangoModelFactory):
    class Meta:
        model = Vote

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        if 'score' not in kwargs:
            kwargs['score'] = randint(1, 10)
        if 'meme' not in kwargs:
            kwargs['meme'] = MemeFactory()
        if 'user' not in kwargs:
            kwargs['user'] = UserFactory()
        return super(VoteFactory, cls)._create(model_class, *args, **kwargs)
