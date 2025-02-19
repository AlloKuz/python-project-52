from django.test import TestCase, Client
from django.shortcuts import reverse

from users.models import User
from tasks.models import Task
from labels.models import Label


class LabelTest(TestCase):
    fixtures = ["sample.json"]

    def setUp(self):
        self.client = Client(headers={"Accept-Language": "en"})
        self.client.login(username="test_user",
                          password="test_password")
        self.user = User.objects.get(username="test_user")
        self.label = Label.objects.get(name="test_label")
        self.task = Task.objects.get(name="test_task")

    def test_unauthorized(self):
        self.client.logout()

        urls = [
            reverse("labels"),
            reverse("labels_create"),
            reverse("labels_update", kwargs={"pk": self.label.id}),
            reverse("labels_delete", kwargs={"pk": self.label.id}),
        ]
        
        for url in urls:
            response = self.client.get(url, follow=True)
            self.assertIn(b"First you need to log in", response.content)
            self.assertEqual(reverse("login"), response.request['PATH_INFO'])

    def test_LabelsView(self):
        response = self.client.get(reverse("labels"))

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Labels", response.content)
        self.assertIn(b"test_label", response.content)

    def test_LabelCreateView(self):
        # POST
        response = self.client.post(reverse("labels_create"),
                                    data={"name": "test_create"},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Label created", response.content)
        self.assertEqual(reverse("labels"), response.request['PATH_INFO'])
        self.assertTrue(Label.objects.filter(name="test_create").exists())

        # GET
        response = self.client.get(reverse("labels_create"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Create label", response.content)

    def test_LabelUpdateView(self):
        url_for_update = reverse("labels_update",
                                 kwargs={"pk": self.label.id})
        # GET
        response = self.client.get(url_for_update)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Edit label", response.content)
        self.assertIn(b"test_label", response.content)

        # POST
        response = self.client.post(url_for_update,
                                    data={"name": "test_updated"},
                                    follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Label updated", response.content)
        self.assertEqual(reverse("labels"), response.request['PATH_INFO'])
        self.assertFalse(Label.objects.filter(name="test_label").exists())
        self.assertTrue(Label.objects.filter(name="test_updated").exists())

    def test_LabelDeleteView(self):
        path_to_label = reverse("labels_delete",
                                kwargs={"pk": self.label.id})
        # when task exists
        response = self.client.post(path_to_label, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Unable to delete label", response.content)
        self.assertTrue(Label.objects.filter(name="test_label").exists())

        # when task removed
        self.label.task_set.all().delete()
    
        response = self.client.post(path_to_label, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Label deleted", response.content)
        self.assertFalse(Label.objects.filter(name="test_label").exists())