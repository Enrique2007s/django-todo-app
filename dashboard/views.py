from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.utils.text import slugify
from .models import Board, Task
from .forms import BoardForm, TaskForm


# Create your views here.
class MyDashboardView(generic.ListView):
    queryset = Board.objects.all()
    template_name = 'dashboard/dashboard.html'
    context_object_name = 'object_list'
    paginate_by = 8

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Board.objects.filter(owner=self.request.user)
        return Board.objects.none()


def deleteBoard(request, slug):
    board = get_object_or_404(Board, slug=slug, owner=request.user)
    if not request.user.is_authenticated:
        return redirect('account_login')
    if request.method == 'POST':
        board_title = board.title
        board.delete()
        messages.success(request, f'Board {board_title} has been deleted.')
        return redirect('my-dashboard')
    return render(request, 'dashboard/delete-board.html', {'board': board},)


def createBoard(request):
    form = BoardForm()
    if request.method == 'POST' and not request.user.is_authenticated:
        return redirect('account_login')
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.owner = request.user

            base_slug = slugify(board.title)
            unique_slug = base_slug
            counter = 1
            while Board.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{base_slug}-{counter}'
                counter += 1

            board.slug = unique_slug
            board.save()
            messages.success(request, f'Board {board.title} has been created.')
            return redirect('my-dashboard')

    return render(request, 'dashboard/create-board.html', {'form': form})


def tasks(request, slug):
    queryset = Board.objects.filter(owner=request.user)
    board = get_object_or_404(queryset, slug=slug)
    tasks = Task.objects.filter(board=board)
    form = TaskForm()
    if request.method == 'POST' and not request.user.is_authenticated:
        return redirect('account_login')
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
    task = get_object_or_404(Task, id=pk, owner=request.user)
    if not request.user.is_authenticated:
        return redirect('account_login')

    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks', slug=task.board.slug)
    return render(request, 'dashboard/update-task.html', {'form': form, 'task': task},)


def deleteTask(request, pk):
    task = get_object_or_404(Task, id=pk, owner=request.user)
    if not request.user.is_authenticated:
        return redirect('account_login')
    if request.method == 'POST':
        task.delete()
        return redirect('tasks', slug=task.board.slug)
    return render(request, 'dashboard/delete-task.html', {'task': task},)
