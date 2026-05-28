from django.contrib import admin
from .models import Board, Comment
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Board)
class BoardAdmin(SummernoteModelAdmin):
    list_display = ('title', 'owner', 'created_on')
    search_fields = ('title', 'owner__username', 'created_on')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('created_on', 'owner')


@admin.register(Comment)
class CommentAdmin(SummernoteModelAdmin):
    list_display = ('owner', 'board', 'created_on')
    search_fields = ('owner__username', 'board__title', 'created_on')
    list_filter = ('created_on', 'owner')


# Register your models here.
