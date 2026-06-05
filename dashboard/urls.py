from . import views
from django.urls import path

urlpatterns = [
    path('', views.MyDashboardView.as_view(), name='my-dashboard'),
    path('boards/<slug:slug>/', views.tasks, name='tasks'),
    path('update-task/<str:pk>/', views.updateTask, name='update-task'),
    path('delete-task/<str:pk>/', views.deleteTask, name='delete-task'),
]
