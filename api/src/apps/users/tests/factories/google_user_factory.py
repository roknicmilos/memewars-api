import factory
from faker import Faker

from apps.users.authentication import GoogleUser

faker = Faker()


class GoogleUserFactory(factory.Factory):
    class Meta:
        model = GoogleUser

    email = factory.LazyAttribute(lambda o: f'{o.given_name}.{o.family_name}@example.rs')
    given_name = factory.LazyAttribute(lambda _: faker.first_name())
    family_name = factory.LazyAttribute(lambda _: faker.last_name())
    picture = factory.LazyAttribute(lambda o: f'https://mock-google-domain/{o.given_name}.{o.family_name}.jpg')
