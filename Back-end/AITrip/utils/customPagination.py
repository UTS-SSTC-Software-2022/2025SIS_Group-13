from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 5 
    page_size_query_param = 'page_size'
    max_page_size = 100

    def paginate_queryset(self, queryset, request, view=None):
        if not request.query_params.get(self.page_query_param) and not request.query_params.get(self.page_size_query_param):
            return None
        return super().paginate_queryset(queryset, request, view)