# posts/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from .pagination import CustomPageNumberPagination

# --- Web Views ---
class PostListView(ListView):
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the request to the context to access GET parameters in the template
        context['request'] = self.request
        return context

    def get_paginate_by(self, queryset):
        # Get the 'per_page' parameter from the query string; default to 5 if not provided
        try:
            per_page = int(self.request.GET.get('per_page', 5))
            # Set a reasonable limit to avoid excessive database queries
            return min(max(per_page, 1), 15)
        except ValueError:
            # Fallback to default if the parameter is not a valid integer
            return 5

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'  # Template for post details
    context_object_name = 'post'

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
