from django.shortcuts import render
from django.views import generic
from .models import Board


# Create your views here.
class MyDashboardView(generic.ListView):
    queryset = Board.objects.all()
    template_name = 'dashboard/dashboard.html'
    context_object_name = 'object_list'
