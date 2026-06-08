from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Comment(models.Model):
    """
    Represents a comment made by a user on the about page,
    containing the owner of the comment,
    related content, and the date it was created.
    The owner is linked to the User model through a ForeignKey relationship,
    """
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'Comment by {self.owner} on about page'
