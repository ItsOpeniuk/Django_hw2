from rest_framework.pagination import CursorPagination


class GeneralPaginator(CursorPagination):
    page_size = 5
    ordering = 'id'
    max_page_size = 20