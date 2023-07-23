from django.contrib import admin

from apps.common.admin import TimestampableModelAdmin
from apps.wars.admin import MemeAdmin
from apps.wars.models import Meme
from apps.wars.tests.factories import MemeFactory
from meme_wars.tests.test_case import TestCase


class TestMemeAdmin(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.meme_admin = MemeAdmin(model=Meme, admin_site=admin.site)

    def test_should_render_pending_approval_status_html(self):
        meme = MemeFactory()
        html_string = self.meme_admin.approval_status_html(obj=meme)
        expected_html_string_part = (
            f'<div class="meme-approval-status meme-approval-status--{Meme.ApprovalStatuses.PENDING}">'
        )
        self.assertIn(expected_html_string_part, html_string)

    def test_should_return_declared_readonly_fields_when_adding_meme(self):
        actual_readonly_fields = self.meme_admin.get_readonly_fields(request=self.get_request_example())
        expected_readonly_fields = ("id",)
        expected_readonly_fields += MemeAdmin.readonly_fields
        expected_readonly_fields += TimestampableModelAdmin.timestampable_fields
        self.assertEqual(sorted(actual_readonly_fields), sorted(expected_readonly_fields))

    def test_should_return_declared_and_additional_readonly_fields_when_adding_meme(self):
        meme = MemeFactory()
        actual_readonly_fields = self.meme_admin.get_readonly_fields(request=self.get_request_example(), obj=meme)
        expected_readonly_fields = ("id",)
        expected_readonly_fields += MemeAdmin.readonly_fields
        expected_readonly_fields += (
            "user",
            "war",
            "total_score",
        )
        expected_readonly_fields += TimestampableModelAdmin.timestampable_fields
        self.assertEqual(sorted(actual_readonly_fields), sorted(expected_readonly_fields))

    def test_queryset_should_contain_user_email_deterministic_annotation(self):
        self.create_and_login_superuser()
        memes = MemeFactory.create_batch(size=3)

        queryset = self.meme_admin.get_queryset(request=self.get_request_example())
        annotated_values = [item.user_email_deterministic for item in queryset]

        user_emails = [meme.user.email for meme in memes]
        self.assertEqual(sorted(annotated_values), sorted(user_emails))
