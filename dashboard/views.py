from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views import generic
from django.utils.text import slugify
from .models import Board, Task
from .forms import BoardForm, TaskForm


# Create your views here.
class MyDashboardView(generic.ListView):
    """
    Displays the user's dashboard with a list of their boards.
    Only authenticated users can see their boards, while
    unauthenticated users will see an empty list

    displays an instance of :model:`Board` for the
    currently logged-in user, ordered by creation date.
    If the user is not authenticated, it returns an empty
    queryset, ensuring that no boards are displayed to unauthenticated users.
    **context**
    ``object_list``:
    A queryset of all Board instances for the currently logged-in user.
    **template**
    ``dashboard/dashboard.html``:
    """
    queryset = Board.objects.all()
    template_name = 'dashboard/dashboard.html'
    context_object_name = 'object_list'
    paginate_by = 8

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Board.objects.filter(owner=self.request.user)
        return Board.objects.none()


def deleteBoard(request, slug):
    """
    Handles the deletion of a board,
    ensuring that only the owner can delete it.
    Provides feedback messages for successful
    deletion and redirects to the dashboard.

    displays an instance of :model:`Board` based on the
    provided slug and the currently logged-in user.
    If the user is not authenticated or does not own the board, it returns
    **context**
    ``board``:
    An instance of Board for users to delete.
    **template**
    ``dashboard/delete-board.html``:
    """
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
    """
    Handles the creation of a new board,
    ensuring that only authenticated users can create boards.
    Generates a unique slug for the
    board based on its title to prevent conflicts.

    displays a form for creating a new :model:`Board`.
    **context**
    ``form``:
    An instance of BoardForm for users to submit new board details.
    **template**
    ``dashboard/create-board.html``:
    """
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
    """
    Displays the tasks for a specific board,
    allowing users to view and add tasks.
    Ensures that only the owner of the board can access its tasks.

    displays an instance of :model:`Board` based on the provided slug and the
    currently logged-in user, along with its related :model:`Task` instances.
    **context**
    ``board``:
    An instance of Board for users to view tasks.
    ``tasks``:
    A queryset of all Task instances related to the board.
    ``form``:
    An instance of TaskForm for users to submit new task details.
    **template**
    ``dashboard/tasks.html``:
    """
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
            messages.success(
                request,
                f'Task "{task.title}" has been added to board.'
            )
            return redirect('tasks', slug=slug)

    return render(
        request,
        'dashboard/tasks.html',
        {'board': board, 'tasks': tasks, 'form': form},
    )


def updateTask(request, pk):
    """
    Handles the updating of a task, ensuring that only the owner can update it.
    Provides feedback messages for successful updates
    and redirects to the task list.

    displays an instance of :model:`Task` based on the provided primary key
    and the currently logged-in user.
    If the user is not authenticated or does not own the task
    **context**
    ``form``:
    An instance of TaskForm pre-filled with the existing task content for
    editing.
    **template**
    ``dashboard/update-task.html``:
    """
    task = get_object_or_404(Task, id=pk, owner=request.user)
    if not request.user.is_authenticated:
        return redirect('account_login')

    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f'Task "{task.title}" has been updated.')
            return redirect('tasks', slug=task.board.slug)
    return render(
        request,
        'dashboard/update-task.html',
        {'form': form, 'task': task},
    )


def deleteTask(request, pk):
    """
    Handles the deletion of a task, ensuring that only the owner can delete it.
    Provides feedback messages for successful
    deletion and redirects to the task list.

    displays an instance of :model:`Task` based on the provided primary key
    and the currently logged-in user.
    If the user is not authenticated or does not own the task
    it returns a 404 error, preventing unauthorized access to task deletion.
    **context**
    ``task``:
    An instance of Task for users to delete.
    **template**
    ``dashboard/delete-task.html``:
    """
    task = get_object_or_404(Task, id=pk, owner=request.user)
    if not request.user.is_authenticated:
        return redirect('account_login')
    if request.method == 'POST':
        task.delete()
        messages.success(request, f'Task "{task.title}" has been deleted.')
        return redirect('tasks', slug=task.board.slug)
    return render(request, 'dashboard/delete-task.html', {'task': task},)
