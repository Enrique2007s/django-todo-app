from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from .models import Board, Task


class BoardModelTest(TestCase):
    def setUp(self):
        # create a test user for ownership
        self.user = User.objects.create_user(
            username='testuser', password='password'
        )
        self.board = Board.objects.create(
            title='Test Board',
            excerpt='This is a test board.',
            owner=self.user,
            slug='test-board',
        )

    def test_board_creation(self):
        self.assertEqual(self.board.title, 'Test Board')
        self.assertEqual(self.board.excerpt, 'This is a test board.')
        self.assertIsNotNone(self.board.created_on)


class TaskModelTest(TestCase):
    def setUp(self):
        # create a test user and board for the task
        self.user = User.objects.create_user(
            username='testuser2', password='password'
        )
        self.board = Board.objects.create(
            title='Test Board',
            excerpt='This is a test board.',
            owner=self.user,
            slug='test-board-2',
        )
        self.task = Task.objects.create(
            title='Test Task', board=self.board, owner=self.user
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.board, self.board)
        self.assertFalse(self.task.is_completed)
        self.assertIsNotNone(self.task.created_on)


class PaginationTest(TestCase):
    def setUp(self):
        # create a user and many boards to trigger pagination
        self.user = User.objects.create_user(
            username='pager', password='password'
        )
        for i in range(10):
            Board.objects.create(
                title=f'Board {i}',
                excerpt='page test',
                owner=self.user,
                slug=f'board-{i}',
            )

    def test_dashboard_pagination(self):
        # login and request first page
        self.client.login(username='pager', password='password')
        url = reverse('my-dashboard')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        page1 = resp.context['page_obj']
        # default paginate_by is 8
        self.assertEqual(len(page1.object_list), 8)
        self.assertEqual(page1.number, 1)

        # request second page
        resp2 = self.client.get(url, {'page': 2})
        self.assertEqual(resp2.status_code, 200)
        page2 = resp2.context['page_obj']
        self.assertEqual(len(page2.object_list), 2)
        self.assertEqual(page2.number, 2)


class BoardAccessTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser2', password='password'
        )
        self.board = Board.objects.create(
            title='Test Board',
            excerpt='This is a test board.',
            owner=self.user,
            slug='test-board-2',
        )
