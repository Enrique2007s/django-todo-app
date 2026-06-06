from . import views
from django.urls import path

urlpatterns = [
    path('', views.MyDashboardView.as_view(), name='my-dashboard'),
    path('create-board/', views.createBoard, name='create-board'),
    path('boards/<slug:slug>/', views.tasks, name='tasks'),
    path('update-task/<str:pk>/', views.updateTask, name='update-task'),
    path('delete-task/<str:pk>/', views.deleteTask, name='delete-task'),
    path('delete-board/<slug:slug>/', views.deleteBoard, name='delete-board'),
]
