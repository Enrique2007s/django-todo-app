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
        return f'Board: {self.title}'


class Task(models.Model):
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='tasks')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'Task: {self.title}, in board: {self.board}, owned by {self.owner}'
