from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostAPIViewSet, PostListView, PostDetailView

router = DefaultRouter()
router.register(r'posts', PostAPIViewSet, basename='post')

urlpatterns = [
    path('api/', include(router.urls)),  # API endpoints
    path('', PostListView.as_view(), name='home'),  # Set this as the 'home' view
    path('posts/', PostListView.as_view(), name='post_list'),  # Web: List view 
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),  # Web: Detail view
]
