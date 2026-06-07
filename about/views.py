from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import Comment
from .forms import CommentForm


# About page view
def about(request):
    comments = Comment.objects.all()
    form = CommentForm()
    if request.method == 'POST' and not request.user.is_authenticated:
        return redirect('account_login')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.owner = request.user
            comment.save()
            messages.success(request, 'Your comment has been added.')
            return redirect('about')
    return render(request, 'about/about.html', {'comments': comments, 'form': form})



# def about(request):
#     return render(request, 'about/about.html')


# # Simple comment form (keeps model import valid)
# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['content']
