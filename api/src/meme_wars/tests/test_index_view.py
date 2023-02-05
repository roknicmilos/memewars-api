from django.urls import reverse

from apps.common.tests import TestCase
from pytest_django.asserts import assertTemplateUsed


class TestIndexView(TestCase):

    def test_should_render_index_page_with_correct_context(self):
        response = self.client.get(path=reverse('index'))
        assertTemplateUsed(response, 'index.html')
