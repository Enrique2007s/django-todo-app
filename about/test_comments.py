from django.test import TestCase
from .forms import CommentForm
from django.contrib.auth.models import User


class TestCommentForm(TestCase):

    def test_form_is_valid(self):
        """Test for the comment form."""
        form = CommentForm({
            'content': 'Hello!'
        })
        self.assertTrue(form.is_valid(), msg="Form is not valid")

    def test_blank_content_invalid(self):
        """ Test that blank content is invalid"""
        form = CommentForm({
            'content': ''
        })
        self.assertFalse(form.is_valid(),
        msg="Form should be invalid for blank content")
        self.assertIn('content', form.errors)
        self.assertEqual(form.errors['content'], ['This field is required.'])

    def test_edit_comment_form_valid(self):
        """Test that the edit comment form is valid with content."""
        self.user = User.objects.create_user(
            username='testuser',
            password='password')

        form = CommentForm({
            'content': 'Updated comment content.'
        })
        self.assertTrue(
            form.is_valid(), msg="Edit form should be valid with content"
        )
