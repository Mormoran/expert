from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)

class ExpertPageNumberPagination(PageNumberPagination):
    page_size = 1000