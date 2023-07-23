from apps.wars.admin import MemeAdmin
from apps.wars.admin.filters import RequiresApprovalFilter
from apps.wars.models import Meme
from apps.wars.tests.factories import MemeFactory, WarFactory
from meme_wars.tests.test_case import TestCase


class TestRequiresApprovalFilter(TestCase):
    def setUp(self) -> None:
        super().setUp()
        first_war = WarFactory(requires_meme_approval=False)
        second_war = WarFactory(requires_meme_approval=True)
        MemeFactory.create_batch(size=2, war=first_war)
        MemeFactory.create_batch(size=3, war=second_war)

    def test_should_return_yes_and_no_options(self):
        requires_approval_filter = RequiresApprovalFilter(
            request=self.get_request_example(), params={}, model=Meme, model_admin=MemeAdmin
        )
        actual_lookups = requires_approval_filter.lookups(request=self.get_request_example(), model_admin=MemeAdmin)
        expected_lookups = [
            (1, "Yes"),
            (0, "No"),
        ]
        self.assertEqual(actual_lookups, expected_lookups)

    def test_should_filter_memes_that_require_approval(self):
        requires_approval_filter = RequiresApprovalFilter(
            request=self.get_request_example(),
            params={RequiresApprovalFilter.parameter_name: 1},
            model=Meme,
            model_admin=MemeAdmin,
        )
        queryset = requires_approval_filter.queryset(
            request=self.get_request_example(),
            queryset=Meme.objects.all(),
        )
        self.assertEqual(queryset.count(), 3)

    def test_should_filter_memes_that_do_not_require_approval(self):
        requires_approval_filter = RequiresApprovalFilter(
            request=self.get_request_example(),
            params={RequiresApprovalFilter.parameter_name: 0},
            model=Meme,
            model_admin=MemeAdmin,
        )
        queryset = requires_approval_filter.queryset(
            request=self.get_request_example(),
            queryset=Meme.objects.all(),
        )
        self.assertEqual(queryset.count(), 2)

    def test_should_not_filter_memes_when_filter_params_are_empty(self):
        requires_approval_filter = RequiresApprovalFilter(
            request=self.get_request_example(), params={}, model=Meme, model_admin=MemeAdmin
        )
        queryset = requires_approval_filter.queryset(
            request=self.get_request_example(),
            queryset=Meme.objects.all(),
        )
        self.assertEqual(queryset.count(), 5)
