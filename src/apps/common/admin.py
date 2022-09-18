from django.contrib.admin import ModelAdmin as BaseModelAdmin


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
            return self.change_form_fields

        return super(ModelAdmin, self).get_fields(request=request, obj=obj)
