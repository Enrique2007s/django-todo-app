from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Comment


# Register your models here.
@admin.register(Comment)
class CommentAdmin(SummernoteModelAdmin):
    """
    Admin interface for the Comment model, providing a user-friendly way to
    manage comments in the Django admin site. It includes features such as
    displaying key fields, searching, and filtering.
    """
    list_display = ('owner', 'created_on')
    search_fields = ('owner__username', 'created_on')
    list_filter = ('created_on', 'owner')
