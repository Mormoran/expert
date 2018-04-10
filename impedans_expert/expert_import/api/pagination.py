from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)

class RunsPageNumberPagination(PageNumberPagination):
    page_size = 10