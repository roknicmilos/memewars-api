from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from meme_wars.tests.test_case import TestCase


class TestIndexView(TestCase):
    def test_should_render_index_page_with_correct_context(self):
        response = self.client.get(path=reverse("index"))
        assertTemplateUsed(response, "index.html")
