from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardPageSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'meta': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'data': data
        })