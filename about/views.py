from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Comment
from .forms import CommentForm


# About page view
def about(request):
    """
    Displays the about page with all comments.
    Handles the submission of new comments, ensuring that only
    authenticated users can post comments.
    Provides feedback messages for successful comment posting
    or if the user is not authenticated.

    displays a list of :model:`Comment` 
    **context**
    ``comments``:
    A queryset of all Comment instancesto be displayed on the about page.
    ``form``:
    An instance of CommentForm for users to submit new comments.
    **template**
    ``about/about.html``:
    """
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
    """
    Allows users to edit their own comments on the about page.
    Ensures that only the owner of the comment can edit it.

    displays an instance of :model:`Comment` based on the provided primary key
    **context**
    ``form``:
    An instance of CommentForm pre-filled with
    the existing comment content for editing.
    **template**
    ``about/edit-comment.html``:
    """
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
    """
    Allows users to delete their own comments on the about page.
    Ensures that only the owner of the comment can delete it.

    displays an instance of :model:`Comment` based on the provided primary key
    **context**
    ``comment``:
    An instance of Comment for users to delete.
    **template**
    ``about/delete-comment.html``:
    """
    comment = get_object_or_404(Comment, id=comment_id, owner=request.user)

    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Your comment has been deleted!')
        return redirect('about')

    return render(request, 'about/delete-comment.html', {'comment': comment})
