from django.test import TestCase
from django.urls import reverse

from users.models import User
from statuses.models import Status
from tasks.models import Task


class TasksTest(TestCase):
    fixtures = ["sample.json"]

    def setUp(self):
        self.client.login(username="test_user",
                          password="test_password")
        self.status = Status.objects.get(name="test_status")
        self.user = User.objects.get(username="test_user")
        self.task = Task.objects.get(name="test_task")

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

        response = self.client.get(reverse("tasks_create"),
                                   headers={"accept-language": "en"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Create task", response.content)

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

    def test_TaskDeleteView(self):
        response = self.client.post(
            reverse("tasks_delete",
                    kwargs={"id": self.task.id}),
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(name="test_task").exists())