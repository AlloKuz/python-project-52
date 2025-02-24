from django.http import HttpResponse
from django.test import Client, TestCase
from django.urls import reverse

from task_manager.load_fixture import load
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


class TasksTest(TestCase):
    fixtures = ["sample.json"]
    data = load("task_manager/fixtures/user_data.json")

    def setUp(self):
        self.client = Client(headers={"Accept-Language": "en"})
        self.client.login(**self.data["user"])
        self.status = Status.objects.get(**self.data["status"])
        self.user = User.objects.get(username=self.data["user"]["username"])
        self.label = Label.objects.get(**self.data["label"])
        self.task = Task.objects.get(**self.data["task"])

    def test_unauthorized(self):
        self.client.logout()

        urls = [
            reverse("tasks"),
            reverse("tasks_create"),
            reverse("tasks_update", kwargs={"pk": self.task.id}),
            reverse("tasks_delete", kwargs={"pk": self.task.id}),
        ]

        for url in urls:
            response = self.client.get(url, follow=True)
            self.assertIn(b"First you need to log in", response.content)
            self.assertRedirects(response, reverse("login") + "?next=" + url)

    def test_TasksView(self):
        response = self.client.get(reverse("tasks"))

        self.assertEqual(response.status_code, HttpResponse.status_code)
        self.assertIn(b"Tasks", response.content)
        self.assertIn(self.task.name.encode(), response.content)

    def test_TaskDetailView(self):
        response = self.client.get(reverse("tasks_show",
                                           kwargs={"pk": self.task.id}))

        self.assertEqual(response.status_code, HttpResponse.status_code)
        self.assertIn(b"Task Detail", response.content)
        self.assertIn(self.task.name.encode(), response.content)
        self.assertIn(self.user.username.encode(), response.content)
        self.assertIn(self.status.name.encode(), response.content)
        self.assertIn(b"Labels", response.content)
        self.assertIn(self.label.name.encode(), response.content)

    def test_TaskCreateView(self):
        # POST
        response = self.client.post(reverse("tasks_create"),
                                    follow=True,
                                    data={"name": "test_task_create",
                                          "status": self.status.id})
        self.assertIn(b"Task created", response.content)
        self.assertRedirects(response, reverse("tasks"))
        self.assertTrue(Task.objects.filter(name="test_task_create").exists())

        # GET
        response = self.client.get(reverse("tasks_create"))
        self.assertEqual(response.status_code, HttpResponse.status_code)
        self.assertIn(b"Create task", response.content)
        self.assertIn(b"Description", response.content)
        self.assertIn(b"Labels", response.content)

    def test_TaskUpdateView(self):
        url_for_update = reverse("tasks_update",
                                 kwargs={"pk": self.task.id})
        # GET
        response = self.client.get(url_for_update)

        self.assertEqual(response.status_code, HttpResponse.status_code)
        self.assertIn(b"Edit task", response.content)
        self.assertIn(self.task.name.encode(), response.content)

        # POST
        response = self.client.post(url_for_update,
                                    follow=True,
                                    data={
                                        "name": "test_task_updated",
                                        "status": self.status.id,
                                    })

        self.assertIn(b"Task updated", response.content)
        self.assertRedirects(response, reverse("tasks"))
        self.assertFalse(Task.objects.filter(
            name=self.task.name.encode()).exists())
        self.assertTrue(Task.objects.filter(
            name="test_task_updated").exists())

    def test_TaskDeleteView(self):
        url_for_delete = reverse("tasks_delete",
                                 kwargs={"pk": self.task.id})

        response = self.client.post(url_for_delete, follow=True)
        self.assertRedirects(response, reverse("tasks"))
        self.assertIn(b"Task deleted", response.content)
        self.assertFalse(Task.objects.filter(name=self.task.name).exists())
