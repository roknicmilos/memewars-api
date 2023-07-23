import factory
from factory.django import DjangoModelFactory
from faker import Faker
from rest_framework.authtoken.models import Token

from apps.users.tests.factories import UserFactory

faker = Faker()


class TokenFactory(DjangoModelFactory):
    class Meta:
        model = Token

    user = factory.LazyAttribute(lambda _: UserFactory())
