from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from apps.common.admin import ModelAdmin
from apps.meme_wars.models import War, VotingScore


class VotingScoreInline(admin.TabularInline):
    model = VotingScore
    extra = 0
    max_num = 5
    fields = ('label', 'order',)
    readonly_fields = ('order',)


@admin.action(description='End selected Wars')
def end_wars(model_admin, request, queryset) -> None:
    queryset.update(has_ended=True)


@admin.action(description='Reopen selected Wars')
def reopen_wars(model_admin, request, queryset) -> None:
    queryset.update(has_ended=False)


@admin.action(description='Publish selected Wars')
def publish_wars(model_admin, request, queryset) -> None:
    queryset.update(is_published=True)


@admin.action(description='Unpublish selected Wars')
def unpublish_wars(model_admin, request, queryset) -> None:
    queryset.update(is_published=False)


@admin.register(War)
class WarAdmin(ModelAdmin):
    list_display = (
        'name', 'id', 'is_published', 'has_ended', 'enlistment_count',
        'meme_count', 'voter_count', 'vote_count', 'created',
    )
    readonly_fields = (
        'id', 'enlistment_count', 'is_published', 'has_ended', 'meme_count',
        'voter_count', 'vote_count', 'created', 'modified',
    )
    add_form_fields = ('name',)
    inlines = [
        VotingScoreInline,
    ]
    actions = [
        end_wars,
        reopen_wars,
        publish_wars,
        unpublish_wars,
    ]

    def enlistment_count(self, obj: War = None) -> int:
        return obj.enlistment_count

    enlistment_count.short_description = _('enlistments')

    def meme_count(self, obj: War = None) -> int:
        return obj.meme_count

    meme_count.short_description = _('memes')

    def voter_count(self, obj: War = None) -> int:
        return obj.voter_count

    voter_count.short_description = _('voters')

    def vote_count(self, obj: War = None) -> int:
        return obj.vote_count

    vote_count.short_description = _('votes')
