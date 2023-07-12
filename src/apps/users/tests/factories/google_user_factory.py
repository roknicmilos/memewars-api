import factory
from faker import Faker

from apps.users.authentication import GoogleUser
from apps.users.tests.factories.utils import build_email

faker = Faker()


class GoogleUserFactory(factory.Factory):
    class Meta:
        model = GoogleUser

    email = factory.LazyAttribute(lambda user: build_email(user=user))
    given_name = factory.LazyAttribute(lambda _: faker.first_name())
    family_name = factory.LazyAttribute(lambda _: faker.last_name())
    picture = factory.LazyAttribute(lambda o: f"https://mock-google-domain/{o.given_name}.{o.family_name}.jpg")
