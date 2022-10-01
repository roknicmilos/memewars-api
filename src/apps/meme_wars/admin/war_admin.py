from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from apps.common.admin import ModelAdmin
from apps.meme_wars.models import War


@admin.register(War)
class WarAdmin(ModelAdmin):
    list_display = (
        'name', 'id', 'phase', 'enlistment_count',
        'meme_count', 'voter_count', 'vote_count', 'created',
    )
    readonly_fields = (
        'id', 'enlistment_count', 'phase', 'meme_count',
        'voter_count', 'vote_count', 'created', 'modified',
    )
    add_form_fields = ('name',)

    def enlistment_count(self, obj: War = None) -> int:
        return obj.enlistments.count()

    enlistment_count.short_description = _('enlistments')

    def meme_count(self, obj: War = None) -> int:
        return obj.memes.count()

    meme_count.short_description = _('memes')

    def voter_count(self, obj: War = None) -> int:
        return obj.voter_count

    voter_count.short_description = _('voters')

    def vote_count(self, obj: War = None) -> int:
        return obj.votes.count()

    vote_count.short_description = _('votes')
