from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Board(models.Model):
    """
    Stores information about a board, including its title,
    slug, owner, creation date, and an optional excerpt.
    related to the Task model through a ForeignKey relationship,
    allowing each board to have multiple tasks.
    """
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
    """
    Represents a task within a board, containing a title, completion status,
    associated board, owner, and creation date.
    related to the Board model through a ForeignKey relationship, 
    allowing each task to be associated with a specific board.
    """
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, related_name='tasks'
    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tasks'
    )
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return (
            f'Task: {self.title}, in board: {self.board}, '
            f'owned by {self.owner}'
        )
