# posts/views.py

from rest_framework.response import Response
from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer
from .pagination import CustomPageNumberPagination

# --- API Views ---
class PostAPIViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = CustomPageNumberPagination  # Use page number pagination

    def list(self, request, *args, **kwargs):
        # Check if pagination parameters are provided
        if not request.query_params.get('page') and not request.query_params.get('per_page'):
            # Return all posts if pagination parameters are missing
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        
        # Otherwise, use the default pagination
        return super().list(request, *args, **kwargs)
