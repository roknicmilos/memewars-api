from django.contrib import admin
from apps.common.tests import TestCase
from apps.wars.admin import MemeAdmin
from apps.wars.models import Meme
from apps.wars.tests.factories import MemeFactory


class TestMemeAdmin(TestCase):

    def test_should_render_pending_approval_status_html(self):
        meme_admin = MemeAdmin(model=Meme, admin_site=admin.site)
        meme = MemeFactory()
        html_string = meme_admin.approval_status_html(obj=meme)
        expected_html_string_part = (
            f'<div class="meme-approval-status meme-approval-status--{Meme.ApprovalStatuses.PENDING}">'
        )
        self.assertIn(expected_html_string_part, html_string)
