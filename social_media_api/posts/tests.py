# posts/tests.py
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from posts.models import Post, Comment

User = get_user_model()

class PostViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass', email='testuser@example.com')
        self.client.force_authenticate(user=self.user)
        self.post_list_url = reverse('post-list')

    def test_create_post(self):
        data = {
            'title': 'Test Post',
            'content': 'This is a test post.'
        }
        response = self.client.post(self.post_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data.get('author'), self.user.username)

    def test_update_post_not_owner(self):
        # Create a post owned by another user
        other_user = User.objects.create_user(username='otheruser', password='otherpass', email='otheruser@example.com')
        post = Post.objects.create(author=other_user, title='Other Post', content='Other content')
        url = reverse('post-detail', kwargs={'pk': post.pk})
        data = {'title': 'Updated Title'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class CommentViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass', email='testuser@example.com')
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(author=self.user, title='Test Post', content='Test content')
        self.comment_list_url = reverse('comment-list')

    def test_create_comment(self):
        data = {
            'content': 'This is a test comment.',
            'post': self.post.pk
        }
        response = self.client.post(self.comment_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], data['content'])
        self.assertEqual(response.data.get('author'), self.user.username)

    def test_delete_comment(self):
        comment = Comment.objects.create(post=self.post, author=self.user, content='Comment to delete')
        url = reverse('comment-detail', kwargs={'pk': comment.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())
