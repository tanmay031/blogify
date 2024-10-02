from django.test import SimpleTestCase
from django.urls import reverse, resolve
from posts.views import PostListView, PostDetailView, PostAPIViewSet


class TestUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        # URL for the home page, which uses PostListView
        url = reverse('home')
        self.assertEqual(resolve(url).func.view_class, PostListView)

    def test_post_list_url_is_resolved(self):
        # URL for the list of posts, which also uses PostListView
        url = reverse('post_list')
        self.assertEqual(resolve(url).func.view_class, PostListView)

    def test_post_detail_url_is_resolved(self):
        # URL for the detail view of a post
        url = reverse('post_detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, PostDetailView)

    def test_post_api_list_url_is_resolved(self):
        # DRF automatically generates 'post-list' URL for PostAPIViewSet
        url = reverse('post-list')
        self.assertEqual(resolve(url).func.cls, PostAPIViewSet)

    def test_post_api_detail_url_is_resolved(self):
        # DRF automatically generates 'post-detail' URL for PostAPIViewSet
        url = reverse('post-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.cls, PostAPIViewSet)
