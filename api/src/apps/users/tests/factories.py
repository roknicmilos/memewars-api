from factory.django import DjangoModelFactory
from faker import Faker
from apps.users.models import User

faker = Faker()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        if 'email' not in kwargs:
            kwargs['email'] = faker.email()
        return super(UserFactory, cls)._create(model_class, *args, **kwargs)
