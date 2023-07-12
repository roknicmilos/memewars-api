from django.contrib.admin import SimpleListFilter
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _


class RequiresApprovalFilter(SimpleListFilter):
    title = _(
        "Requires approval",
    )
    parameter_name = "requires_approval"

    def lookups(self, request, model_admin):
        return [
            (1, _("Yes")),
            (0, _("No")),
        ]

    def queryset(self, request, queryset: QuerySet):
        value = self.value()
        if value is not None:
            requires_approval = str(value) == "1"
            return queryset.filter(war__requires_meme_approval=requires_approval)
        return queryset
