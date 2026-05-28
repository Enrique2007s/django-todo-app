from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Board(models.Model):
    title = models.CharField(max_length=65)
    slug = models.SlugField(max_length=65, unique=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='boards'
    )
    created_on = models.DateTimeField(auto_now_add=True)
    excerpt = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'Board: {self.title}, owned by {self.owner}'


class Comment(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='comments')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'Comment by {self.owner} on {self.board}'
