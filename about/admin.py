from django.contrib import admin
from .models import Comment
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.
@admin.register(Comment)
class CommentAdmin(SummernoteModelAdmin):
    list_display = ('owner', 'created_on')
    search_fields = ('owner__username', 'created_on')
    list_filter = ('created_on', 'owner')