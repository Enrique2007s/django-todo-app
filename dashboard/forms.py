from django import forms
from django.forms import ModelForm
from .models import Board, Task, Comment


class BoardForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Board title'}))
    excerpt = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Short description', 'rows': 3}),
    )

    class Meta:
        model = Board
        fields = ['title', 'excerpt']


class TaskForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Add a new task here!'}))

    class Meta:
        model = Task
        fields = ['title', 'is_completed']
