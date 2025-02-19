from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
import logging

from statuses.models import Status
from tasks.models import Task

logger = logging.getLogger(__name__)

USER = {"username": "test_user"}
LOGIN_DATA = {
    "username": USER["username"],
    "password": USER["username"]
}
STATUS = {"name": "test_status"}


class TasksTest(TestCase):

    def setUp(self):
        if not User.objects.filter(**USER).exists():
            User.objects.create_user(**LOGIN_DATA)

        self.client = Client()
        self.client.login(**LOGIN_DATA)

        self.status = Status.objects.create(**STATUS)
        self.user = User.objects.get(**USER)
        self.task = Task.objects.create(
            name="test_task",
            status=self.status,
            author=self.user,
        )

    def tearDown(self):
        if self.task:
            self.task.delete()

        user = User.objects.filter(**USER)
        if user.exists():
            user.delete()

        status = Status.objects.filter(**STATUS)
        if status.exists():
            status.delete()

    def test_unauthorized(self):
        self.client.logout()

        response = self.client.get(reverse("tasks"))

        self.assertEqual(response.status_code, 302)

    def test_TasksView(self):

        response = self.client.get(reverse("tasks"))

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"ID", response.content)
        self.assertIn(b"test_task", response.content)

    def test_TasksCreateView(self):
        self.client.post(
            reverse("tasks_create"),
            data={
                "name": "test_task_create",
                "status": self.status.id,
            }
        )

        new_task = Task.objects.filter(name="test_task_create")
        self.assertTrue(new_task.exists())

        response = self.client.get(
            reverse("tasks_create"),
            headers={"accept-language": "en"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Create task", response.content)

        Task.objects.get(name="test_task_create").delete()

    def test_TaskUpdateView(self):
        response = self.client.get(
            reverse("tasks_update",
                    kwargs={"id": self.task.id}),
            headers={"accept-language": "en"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"test_task", response.content)

        response = self.client.post(
            reverse("tasks_update",
                    kwargs={"id": self.task.id}),
            headers={"accept-language": "en"},
            data={
                "name": "test_task_updated",
                "status": self.status.id,
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(Task.objects.filter(name="test_task").exists())
        self.assertTrue(Task.objects.filter(name="test_task_updated").exists())

        Task.objects.filter(name="test_task_updated").delete()

    def test_TaskDeleteView(self):
        response = self.client.post(
            reverse("tasks_delete",
                    kwargs={"id": self.task.id}),
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(name="test_task").exists())