from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """
    A form for creating and updating Comment instances, with a custom widget
    for the content field to enhance user experience when submitting
    comments on the about page.
    """
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Write your comment here...',
                'rows': 4,
                'class': 'form-control',
            }),
        }
        labels = {
            'content': '',
        }
