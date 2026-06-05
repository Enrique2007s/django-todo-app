from django import forms
from django.forms import ModelForm
from .models import Board, Task, Comment


class TaskForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Add a new task here!'}))

    class Meta:
        model = Task
        fields = ['title', 'is_completed']
