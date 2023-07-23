from django.contrib import admin

from apps.common.models import BaseModel


class TimestampableModelAdmin(admin.ModelAdmin):
    timestampable_fields = (
        "created",
        "modified",
    )

    def get_fields(self, request, obj=None):
        fields = list(super().get_fields(request=request, obj=obj))
        if issubclass(self.model, BaseModel):
            for field in self.timestampable_fields:
                if field in fields:
                    fields.remove(field)
                fields.append(field)

        return tuple(fields)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request=request, obj=obj)
        for field in self.timestampable_fields:
            if field not in readonly_fields:
                readonly_fields += (field,)
        return readonly_fields
