from django.contrib import admin
from django.contrib.sessions.models import Session


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    pass
