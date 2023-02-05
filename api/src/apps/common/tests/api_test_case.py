from rest_framework.test import APITestCase as BaseAPITestCase
from apps.common.tests import APIClient


class APITestCase(BaseAPITestCase):
    client_class = APIClient
    client: APIClient

    def setUp(self) -> None:
        super(APITestCase, self).setUp()
        self.maxDiff = None
