from django.contrib.admin import ModelAdmin as BaseModelAdmin
from django.utils.translation import gettext_lazy as _
from apps.common.models import BaseModel


class ModelAdmin(BaseModelAdmin):
    add_form_fieldsets: tuple = None
    change_form_fieldsets: tuple = None
    add_form_fields: tuple = None
    change_form_fields: tuple = None

    def get_fieldsets(self, request, obj=None):
        if not obj and self.add_form_fieldsets is not None:
            return self.add_form_fieldsets

        if obj and self.change_form_fieldsets is not None:
            return self.change_form_fieldsets

        return super(ModelAdmin, self).get_fieldsets(request=request, obj=obj)

    def get_fields(self, request, obj=None):
        if not obj and self.add_form_fields is not None:
            return self.add_form_fields

        if obj and self.change_form_fields is not None:
            fields = self.change_form_fields
        else:
            fields = super(ModelAdmin, self).get_fields(request=request, obj=obj)

        fields = list(fields)
        if 'id' in fields:
            fields.remove('id')
        fields.insert(0, 'id')

        return tuple(fields)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super(ModelAdmin, self).get_readonly_fields(request=request, obj=obj))
        if 'id' not in readonly_fields:
            readonly_fields.append('id')
        return tuple(readonly_fields)

    def admin_id(self, obj: BaseModel = None) -> str:
        return f'{obj.verbose_name} {obj.pk}'

    admin_id.short_description = _('id')
