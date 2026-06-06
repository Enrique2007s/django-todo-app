from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Board, Task
from .forms import TaskForm


# Create your views here.
class MyDashboardView(generic.ListView):
    queryset = Board.objects.all()
    template_name = 'dashboard/dashboard.html'
    context_object_name = 'object_list'
    paginate_by = 8

    def get_queryset(self):
        return Board.objects.filter(owner=self.request.user)


def deleteBoard(request, slug):
    board = get_object_or_404(Board, slug=slug)
    if request.method == 'POST':
        board_title = board.title
        board.delete()
        messages.success(request, f'Board {board_title} has been deleted.')
        return redirect('my-dashboard')
    return render(request, 'dashboard/delete-board.html', {'board': board},)


def tasks(request, slug):
    queryset = Board.objects.filter(owner=request.user)
    board = get_object_or_404(queryset, slug=slug)
    tasks = Task.objects.filter(board=board)
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.board = board
            task.owner = request.user
            task.save()
        return redirect('tasks', slug=slug)

    return render(request, 'dashboard/tasks.html', {'board': board, 'tasks': tasks, 'form': form},)


def updateTask(request, pk):
    task = Task.objects.get(id=pk)

    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks', slug=task.board.slug)
    return render(request, 'dashboard/update-task.html', {'form': form, 'task': task},)


def deleteTask(request, pk):
    task = Task.objects.get(id=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks', slug=task.board.slug)
    return render(request, 'dashboard/delete-task.html', {'task': task},)
