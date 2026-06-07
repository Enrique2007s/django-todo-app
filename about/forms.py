from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
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
