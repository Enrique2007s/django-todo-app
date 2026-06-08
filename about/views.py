from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Comment
from .forms import CommentForm


# About page view
def about(request):
    # Get all comments (ordered by newest first from model Meta)
    comments = Comment.objects.all()

    # Handle comment submission
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(
                request, 'You must be logged in to leave a comment.'
            )
            return redirect('{ url "account_login" }')

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.owner = request.user
            comment.save()
            messages.success(request, 'Your comment has been posted!')
            return redirect('about')
    else:
        form = CommentForm()

    context = {
        'comments': comments,
        'form': form,
    }
    return render(request, 'about/about.html', context)


# Edit comment view
@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, owner=request.user)

    # Check if the logged in user is the owner of the comment
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your comment has been updated!')
            return redirect('about')
    else:
        form = CommentForm(instance=comment)

    return render(request, 'about/edit-comment.html', {'form': form})


# Delete comment view
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, owner=request.user)

    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Your comment has been deleted!')
        return redirect('about')

    return render(request, 'about/delete-comment.html', {'comment': comment})
