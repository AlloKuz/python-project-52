from django.test import TestCase, Client
from django.urls import reverse
import logging

from statuses.models import Status

logger = logging.getLogger(__name__)


class StatusViewTest(TestCase):
    fixtures = ["sample.json"]

    def setUp(self):
        self.client = Client(headers={"Accept-Language": "en"})
        self.client.login(username="test_user",
                          password="test_password")
        self.status = Status.objects.get(name="test_status")

    def test_unauthorized(self):
        self.client.logout()

        urls = [
            reverse("statuses"),
            reverse("statuses_create"),
            reverse("statuses_update", kwargs={"pk": self.status.id}),
            reverse("statuses_delete", kwargs={"pk": self.status.id}),
        ]

        for url in urls:
            response = self.client.get(url, follow=True)
            self.assertIn(b"First you need to log in", response.content)
            self.assertEqual(reverse("login"), response.request['PATH_INFO'])

    def test_StatusesView(self):
        response = self.client.get(reverse("statuses"))

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Statuses", response.content)
        self.assertIn(b"test_status", response.content)

    def test_StatusCreateView(self):
        # POST
        response = self.client.post(reverse("statuses_create"),
                                    data={"name": "new_test_status"},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Status created", response.content)
        self.assertEqual(reverse("statuses"), response.request['PATH_INFO'])
        self.assertTrue(Status.objects.filter(name="new_test_status").exists())

        # GET
        response = self.client.get(reverse("statuses"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Create status", response.content)

    def test_StatusUpdateView(self):
        path_to_status_update = reverse("statuses_update",
                                        kwargs={"pk": self.status.id})
        # GET
        response = self.client.get(path_to_status_update, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Edit status", response.content)
        self.assertIn(b"test_status", response.content)

        # POST
        response = self.client.post(path_to_status_update,
                                    data={"name": "test_updated"},
                                    follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Status updated", response.content)
        self.assertEqual(reverse("statuses"), response.request['PATH_INFO'])
        self.assertTrue(Status.objects.filter(name="test_updated").exists())
        self.assertFalse(Status.objects.filter(name="test_status").exists())

    def test_delete(self):
        path_to_object = reverse("statuses_delete",
                                 kwargs={"pk": self.status.id})
        # if task exists
        response = self.client.post(path_to_object, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Unable to delete status", response.content)
        self.assertTrue(Status.objects.filter(name="test_status").exists())

        # remove tasks
        self.status.task_set.all().delete()

        response = self.client.post(path_to_object, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Status deleted", response.content)
        self.assertFalse(Status.objects.filter(name="test_status").exists())