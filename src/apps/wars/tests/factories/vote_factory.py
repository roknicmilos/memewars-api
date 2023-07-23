from random import randint

import factory
from factory.django import DjangoModelFactory
from faker import Faker

from apps.users.tests.factories import UserFactory
from apps.wars.models import Vote
from apps.wars.tests.factories import MemeFactory

faker = Faker()


class VoteFactory(DjangoModelFactory):
    class Meta:
        model = Vote

    score = factory.LazyAttribute(lambda _: randint(1, 10))
    meme = factory.LazyAttribute(lambda _: MemeFactory())
    user = factory.LazyAttribute(lambda _: UserFactory())
