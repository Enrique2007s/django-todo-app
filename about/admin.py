from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Comment


# Register your models here.
@admin.register(Comment)
class CommentAdmin(SummernoteModelAdmin):
    list_display = ('owner', 'created_on')
    search_fields = ('owner__username', 'created_on')
    list_filter = ('created_on', 'owner')
