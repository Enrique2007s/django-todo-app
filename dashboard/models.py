from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Board(models.Model):
    title = models.CharField(max_length=15)
    slug = models.SlugField(max_length=15, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards')
    created_on = models.DateTimeField(auto_now_add=True)