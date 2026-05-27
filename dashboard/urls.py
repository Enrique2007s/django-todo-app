from .  import views
from django.urls import path

urlpatterns = [
    path('', views.MyDashboardView.as_view(), name='my-dashboard'),
]