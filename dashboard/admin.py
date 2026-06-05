from django.contrib import admin
from .models import Board, Comment, Task
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.
@admin.register(Board)
class BoardAdmin(SummernoteModelAdmin):
    list_display = ('title', 'owner', 'created_on')
    search_fields = ('title', 'owner__username', 'created_on')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('created_on', 'owner')


@admin.register(Task)
class TaskAdmin(SummernoteModelAdmin):
    list_display = ('title', 'board', 'owner', 'is_completed', 'created_on')
    search_fields = ('title', 'board__title', 'owner__username', 'created_on')
    list_filter = ('is_completed', 'created_on', 'owner')


@admin.register(Comment)
class CommentAdmin(SummernoteModelAdmin):
    list_display = ('owner', 'board', 'created_on')
    search_fields = ('owner__username', 'board__title', 'created_on')
    list_filter = ('created_on', 'owner')
