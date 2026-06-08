from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Comment(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'Comment by {self.owner} on about page'
