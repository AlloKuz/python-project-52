from django.test import TestCase, Client
from django.urls import reverse

from task_manager.users.models import User
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class TasksTest(TestCase):
    fixtures = ["sample.json"]

    def setUp(self):
        self.client = Client(headers={"Accept-Language": "en"})
        self.client.login(username="test_user",
                          password="test_password")
        self.status = Status.objects.get(name="test_status")
        self.user = User.objects.get(username="test_user")
        self.task = Task.objects.get(name="test_task")

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
            self.assertEqual(reverse("login"), response.request['PATH_INFO'])

    def test_TasksView(self):
        response = self.client.get(reverse("tasks"))

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Tasks", response.content)
        self.assertIn(b"test_task", response.content)

    def test_TaskDetailView(self):
        response = self.client.get(reverse("tasks_show",
                                           kwargs={"pk": self.task.id}))

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Task Detail", response.content)
        self.assertIn(b"test_task", response.content)
        self.assertIn(b"test_user", response.content)
        self.assertIn(b"test_status", response.content)
        self.assertIn(b"Labels", response.content)
        self.assertIn(b"test_label", response.content)

    def test_TaskCreateView(self):
        # POST
        response = self.client.post(reverse("tasks_create"),
                                    follow=True,
                                    data={"name": "test_task_create",
                                          "status": self.status.id})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Task created", response.content)
        self.assertEqual(reverse("tasks"), response.request['PATH_INFO'])
        self.assertTrue(Task.objects.filter(name="test_task_create").exists())

        # GET
        response = self.client.get(reverse("tasks_create"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Create task", response.content)
        self.assertIn(b"Description", response.content)
        self.assertIn(b"Labels", response.content)

    def test_TaskUpdateView(self):
        url_for_update = reverse("tasks_update",
                                 kwargs={"pk": self.task.id})
        # GET
        response = self.client.get(url_for_update)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Edit task", response.content)
        self.assertIn(b"test_task", response.content)

        # POST
        response = self.client.post(url_for_update,
                                    follow=True,
                                    data={
                                        "name": "test_task_updated",
                                        "status": self.status.id,
                                    })

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Task updated", response.content)
        self.assertEqual(reverse("tasks"), response.request['PATH_INFO'])
        self.assertFalse(Task.objects.filter(name="test_task").exists())
        self.assertTrue(Task.objects.filter(name="test_task_updated").exists())

    def test_TaskDeleteView(self):
        url_for_delete = reverse("tasks_delete",
                                 kwargs={"pk": self.task.id})

        response = self.client.post(url_for_delete, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Task deleted", response.content)
        self.assertFalse(Task.objects.filter(name="test_task").exists())