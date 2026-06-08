from django.urls import path

from . import views


urlpatterns = [
 path('', views.about, name='about'),

 path(
    'edit-comment/<int:comment_id>/',
    views.edit_comment, name='edit-comment'),

 path(
    'delete-comment/<int:comment_id>/',
    views.delete_comment, name='delete-comment'),

]
