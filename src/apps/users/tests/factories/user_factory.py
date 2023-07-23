import factory
from factory.django import DjangoModelFactory
from faker import Faker

from apps.users.models import User
from apps.users.tests.factories.utils import build_email

faker = Faker()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.LazyAttribute(lambda user: build_email(user=user))
    first_name = factory.LazyAttribute(lambda _: faker.first_name())
    last_name = factory.LazyAttribute(lambda _: faker.last_name())
