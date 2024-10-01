# posts/tests/test_api_views.py

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from posts.models import Post
from posts.serializers import PostSerializer

class PostAPIViewSetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(30):
            Post.objects.create(title=f'Test Post {i}', content=f'Content for post {i}.')

    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse('post-list')
        self.detail_url = lambda pk: reverse('post-detail', kwargs={'pk': pk})
        self.post1 = Post.objects.first()

    def test_list_all_posts(self):
        response = self.client.get(self.list_url)
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_new_post(self):
        data = {'title': 'New Post', 'content': 'Content of the new post'}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 31)
        self.assertEqual(response.data['title'], 'New Post')
        self.assertEqual(response.data['content'], 'Content of the new post')

    def test_retrieve_single_post(self):
        response = self.client.get(self.detail_url(self.post1.pk))
        post = Post.objects.get(pk=self.post1.pk)
        serializer = PostSerializer(post)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_existing_post(self):
        data = {'title': 'Updated Title', 'content': 'Updated content'}
        response = self.client.put(self.detail_url(self.post1.pk), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.title, 'Updated Title')
        self.assertEqual(self.post1.content, 'Updated content')

    def test_delete_post(self):
        response = self.client.delete(self.detail_url(self.post1.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(pk=self.post1.pk).exists())

    def test_post_api_pagination(self):
        response = self.client.get(self.list_url, {'per_page': 3})
        self.assertEqual(len(response.data['results']), 3)
        response = self.client.get(self.list_url, {'per_page': 30})
        self.assertEqual(len(response.data['results']), 15)

    def test_post_api_invalid_page(self):
        response = self.client.get(self.list_url, {'page': 999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['msg'], 'Page number is invalid. Please provide a valid page number.')
