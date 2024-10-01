# posts/tests/test_web_views.py

from django.test import TestCase
from django.urls import reverse
from posts.models import Post

class PostListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(20):
            Post.objects.create(title=f'Test Post {i}', content=f'This is content for post {i}.')

    def test_post_list_view_status_code(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)

    def test_post_list_view_template(self):
        response = self.client.get(reverse('post_list'))
        self.assertTemplateUsed(response, 'posts/index.html')

    def test_post_list_view_pagination(self):
        response = self.client.get(reverse('post_list'), {'per_page': 5})
        self.assertEqual(len(response.context['posts']), 5)
        response = self.client.get(reverse('post_list'), {'per_page': 'invalid'})
        self.assertEqual(len(response.context['posts']), 5)
        response = self.client.get(reverse('post_list'), {'per_page': 30})
        self.assertEqual(len(response.context['posts']), 15)

class PostDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.post = Post.objects.create(title='Test Post', content='This is a test post.')

    def test_post_detail_view_status_code(self):
        response = self.client.get(reverse('post_detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_view_template(self):
        response = self.client.get(reverse('post_detail', kwargs={'pk': self.post.pk}))
        self.assertTemplateUsed(response, 'posts/post_detail.html')

    def test_post_detail_view_context(self):
        response = self.client.get(reverse('post_detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.context['post'], self.post)
    
    def test_post_detail_view_404_for_nonexistent_post(self):
        response = self.client.get(reverse('post_detail', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)
