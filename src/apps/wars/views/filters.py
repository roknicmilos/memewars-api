from django_filters import rest_framework as filters

from apps.wars.models import Vote


class VoteFilterSet(filters.FilterSet):
    war = filters.CharFilter(field_name="meme__war", lookup_expr="exact")

    class Meta:
        model = Vote
        fields = ["user", "war", "meme"]
