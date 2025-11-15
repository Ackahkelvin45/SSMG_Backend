from rest_framework.pagination import PageNumberPagination

class DefaultPagination(PageNumberPagination):
    page_size = 60 # default items per page
    page_size_query_param = 'page_size'  # allows ?page_size=20
    max_page_size = 100
