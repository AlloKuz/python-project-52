from django.test import TestCase, Client
from django.shortcuts import reverse

from users.models import User
from tasks.models import Task
from labels.models import Label
from statuses.models import Status


USER = {"username": "test_user"}
LOGIN_DATA = {
    "username": USER["username"],
    "password": USER["username"]
}
STATUS = {"name": "test_status"}


class LabelTest(TestCase):

    def setUp(self):
        if not User.objects.filter(**USER).exists():
            User.objects.create_user(**LOGIN_DATA)

        self.client = Client()
        self.client.login(**LOGIN_DATA)

        self.status = Status.objects.create(**STATUS)
        self.user = User.objects.get(**USER)
        self.label = Label.objects.create(name="test_label")
        self.task = Task.objects.create(
            name="test_task",
            status=self.status,
            author=self.user,
        )
        self.task.labels.set([self.label])

    def tearDown(self):
        if self.task:
            self.task.delete()

        user = User.objects.filter(**USER)
        if user.exists():
            self.user.delete()

        status = Status.objects.filter(**STATUS)
        if status.exists():
            self.status.delete()

        label = Label.objects.filter(name="test_label")
        if label.exists():
            self.label.delete()

    def test_unauthorized(self):
        self.client.logout()

        response = self.client.get(reverse("labels"))

        self.assertEqual(response.status_code, 302)

    def test_LabelsView(self):

        response = self.client.get(reverse("labels"))

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"ID", response.content)
        self.assertIn(b"test_label", response.content)

    def test_LabelCreateView(self):
        self.client.post(
            reverse("labels_create"),
            data={
                "name": "test_label_create",
            }
        )

        new_label = Label.objects.filter(name="test_label_create")
        self.assertTrue(new_label.exists())

        response = self.client.get(
            reverse("labels_create"),
            headers={"accept-language": "en"},
        )
        self.assertEqual(response.status_code, 200)

        Label.objects.get(name="test_label_create").delete()

    def test_LabelUpdateView(self):
        response = self.client.get(
            reverse("labels_update",
                    kwargs={"id": self.label.id}),
            headers={"accept-language": "en"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"test_label", response.content)

        response = self.client.post(
            reverse("labels_update",
                    kwargs={"id": self.label.id}),
            headers={"accept-language": "en"},
            data={
                "name": "test_label_updated",
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(Label.objects.filter(name="test_label").exists())
        self.assertTrue(Label.objects.filter(
            name="test_label_updated").exists())

        Label.objects.filter(name="test_label_updated").delete()

    def test_LabelDeleteView(self):
        response = self.client.post(
            reverse("labels_delete",
                    kwargs={"id": self.label.id}),
            headers={"accept-language": "en"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name="test_label").exists())

        self.label.task_set.all().delete()
        response = self.client.post(
            reverse("labels_delete",
                    kwargs={"id": self.label.id}),
            headers={"accept-language": "en"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(name="test_label").exists())