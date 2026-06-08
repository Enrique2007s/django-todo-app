from django import forms
from .models import Board, Task


class BoardForm(forms.ModelForm):
    """
    A form for creating and updating Board instances, with custom widgets
    for the title and excerpt fields to enhance user experience.
    """
    title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Board title'})
    )
    excerpt = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': 'Short description', 'rows': 3}
        ),
    )

    class Meta:
        model = Board
        fields = ['title', 'excerpt']


class TaskForm(forms.ModelForm):
    """
    A form for creating and updating Task instances, with a custom widget
    for the title field to enhance user experience.
    """
    title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Add a new task here!'}),
        error_messages={
            'max_length': 'Task is too long. Please shorten it and try again.'
        },
    )

    class Meta:
        model = Task
        fields = ['title', 'is_completed']
