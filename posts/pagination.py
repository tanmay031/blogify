from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 5  # Default page size
    page_size_query_param = 'per_page'  # Allows clients to set page size in the request
    max_page_size = 15  # Maximum page size limit

    def paginate_queryset(self, queryset, request, view=None):
        try:
            # Attempt to paginate the queryset as usual
            return super().paginate_queryset(queryset, request, view=view)
        except NotFound:
            # Raise a custom error message when an invalid page number is requested
            raise NotFound({'msg': 'Page number is invalid. Please provide a valid page number.'})
