from django.shortcuts import render, redirect
from django import forms
from .models import Comment


# About page view
def about(request):
    return render(request, 'about/about.html')


# Simple comment form (keeps model import valid)
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
