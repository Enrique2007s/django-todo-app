from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from .forms import CommentForm
from .models import Comment


class TestCommentViews(TestCase):

    def setUp(self):

        """Set up a test user and a comment for testing the about page views."""

        self.user = User.objects.create_superuser(
            username="weird-tester",
            password="password123",
            email="weird-tester@example.com"
        )
        self.comment = Comment(
            content="This is a test comment.",
            owner=self.user)
        self.comment.save()

    def test_about_page_loads(self):

        """Test that the about page loads correctly."""

        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about/about.html')
        self.assertContains(response, 'This is a test comment.')

    def test_comment_submission(self):

        """Test that a logged in user can submit a comment."""

        self.client.login(username='weird-tester', password='password123')
        response = self.client.post(reverse('about'), {
            'content': 'Another test comment.'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your comment has been posted!')
        self.assertContains(response, 'Another test comment.')
