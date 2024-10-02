from django.test import TestCase
from django.utils import timezone
from posts.models import Post

class PostModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create sample posts for testing
        cls.post1 = Post.objects.create(title='First Post', content='Content for the first post.')
        cls.post2 = Post.objects.create(title='Second Post', content='Content for the second post.')

    def test_string_representation(self):
        # Test the __str__ method of the Post model
        post = Post(title='Sample Post')
        self.assertEqual(str(post), 'Sample Post')       

    def test_title_max_length(self):
        # Test if the title field has the correct max_length
        post = Post.objects.get(id=self.post1.id)
        max_length = post._meta.get_field('title').max_length
        self.assertEqual(max_length, 255)

    def test_created_at_auto_now_add(self):
        # Test if created_at is automatically set
        post = Post.objects.get(id=self.post1.id)
        self.assertIsNotNone(post.created_at)
        self.assertAlmostEqual(post.created_at, timezone.now(), delta=timezone.timedelta(seconds=10))

    def test_updated_at_auto_now(self):
        # Test if updated_at is automatically updated
        post = Post.objects.get(id=self.post1.id)
        old_updated_at = post.updated_at
        # Update the post
        post.title = 'Updated Title'
        post.save()
        # Fetch the post again
        post.refresh_from_db()
        self.assertNotEqual(post.updated_at, old_updated_at)
