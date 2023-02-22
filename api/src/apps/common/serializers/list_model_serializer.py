from rest_framework.serializers import ListSerializer


class ListModelSerializer(ListSerializer):

    def __init__(self, request=None, total_items: int = None, total_pages: int = None, **kwargs):
        super(ListModelSerializer, self).__init__(**kwargs)
        self.request = request
        self.total_items = total_items
        self.total_pages = total_pages

    @property
    def data(self):
        return {
            'items': super(ListModelSerializer, self).data,
            'pagination': {
                'total_items': self.total_items,
                'total_pages': self.total_pages
            },
        }
