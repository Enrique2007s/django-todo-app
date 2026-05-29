from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Board


# Create your views here.
class MyDashboardView(generic.ListView):
    queryset = Board.objects.all()
    template_name = 'dashboard/dashboard.html'
    context_object_name = 'object_list'
    paginate_by = 8

    def get_queryset(self):
        return Board.objects.filter(owner=self.request.user)


def tasks(request, slug):
    queryset = Board.objects.filter(owner=request.user)
    board = get_object_or_404(queryset, slug=slug)
    return render(request, 'dashboard/tasks.html', {'board': board},)
