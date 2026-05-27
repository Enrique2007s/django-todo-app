from django.contrib import admin
from .models import Board, Comment
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Board)
class BoardAdmin(SummernoteModelAdmin):
    list_display = ('title', 'owner', 'created_on')
    search_fields = ('title', 'owner__username')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comment)
class CommentAdmin(SummernoteModelAdmin):
    list_display = ('author', 'board', 'created_on')
    search_fields = ('author__username', 'board__title')
# Register your models here.
