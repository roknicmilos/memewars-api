from uuid import uuid4

from django.test import Client
import factory
from faker import Faker

from apps.users.models import LoginInProgress


faker = Faker()


class LoginInProgressFactory(factory.Factory):
    class Meta:
        model = LoginInProgress

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        request = Client().get(path="/").wsgi_request
        request.session[LoginInProgress.session_key] = {
            "google_auth_state": uuid4().hex,
            "login_success_redirect_url": faker.url(),
            "login_failure_redirect_url": faker.url(),
        }
        kwargs["request"] = request
        return super()._create(model_class, *args, **kwargs)
