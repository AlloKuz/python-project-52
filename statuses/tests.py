import unittest

from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
import logging

from statuses.models import Status

logger = logging.getLogger(__name__)


class StatusViewTest(unittest.TestCase):

    def setUp(self):
        if not User.objects.filter(username="test_user").exists():
            User.objects.create_user(username="test_user",
                                     password="test_password")

        self.client = Client()
        self.client.login(username="test_user",
                          password="test_password")
        Status.objects.create(name="test_status")

    def tearDown(self):
        if User.objects.filter(username="test_user").exists():
            User.objects.get(username="test_user").delete()
        if Status.objects.filter(name="test_status").exists():
            Status.objects.get(name="test_status").delete()

    def test_read_unauthorized(self):

        self.client.logout()

        response = self.client.get(reverse("statuses"))

        self.assertEqual(response.status_code, 302)
        # self.assertIn(b"alert-danger", response.content)

    def test_read_authorized(self):

        response = self.client.get(reverse("statuses"))

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"test_status", response.content)

    def test_create(self):

        self.client.post(reverse("statuses_create"),
                         data={"name": "new_test_status"})

        response = self.client.get(reverse("statuses"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Status.objects.filter(name="new_test_status").exists())

        Status.objects.filter(name="new_test_status").delete()

    def test_update(self):

        status = Status.objects.get(name="test_status")
        response = self.client.get(reverse("statuses_update",
                                           kwargs={"id": status.id}))

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"test_status", response.content)

        response = self.client.post(reverse("statuses_update",
                                            kwargs={"id": status.id}),
                                    data={"name": "test_status_updated"})

        self.assertTrue(Status.objects.filter(name="test_status_updated")
                        .exists())
        self.assertFalse(Status.objects.filter(name="test_status").exists())

        Status.objects.filter(name="test_status_updated").delete()

    def test_delete(self):

        status = Status.objects.get(name="test_status")

        self.client.post(reverse("statuses_delete",
                                 kwargs={"id": status.id}))

        self.assertFalse(Status.objects.filter(name="test_status").exists())


if __name__ == '__main__':
    unittest.main()