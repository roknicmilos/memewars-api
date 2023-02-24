import math
from django.db.models import QuerySet


class Paginator:
    DEFAULT_ITEMS_PER_PAGE = 50
    PAGE_NUMBER_URL_PARAM_KEY = 'page'
    ITEMS_PER_PAGE_URL_PARAM_KEY = 'ipp'

    def __init__(self, queryset: QuerySet, request):
        self.queryset = queryset
        url_params = request.query_params
        self.page_number = int(url_params.get(self.PAGE_NUMBER_URL_PARAM_KEY, 1))
        self.items_per_page = int(url_params.get(self.ITEMS_PER_PAGE_URL_PARAM_KEY, self.DEFAULT_ITEMS_PER_PAGE))

    @property
    def page(self) -> QuerySet:
        limit = self.items_per_page * self.page_number
        offset = limit - self.items_per_page
        return self.queryset[offset:limit]

    @property
    def total_pages(self) -> int:
        return math.ceil(self.total_items / self.items_per_page) if self.items_per_page else self.total_items

    @property
    def total_items(self) -> int:
        return self.queryset.count()
