import unittest

from django.test import Client
from django.urls import reverse
import logging

from users.models import User

logger = logging.getLogger(__name__)


class UsersViewTest(unittest.TestCase):
    # Test: task_manager.views.UsersView

    def setUp(self):
        User.objects.create_user(first_name="test_username",
                                 username="test_user",
                                 password="test_password")

    def tearDown(self):
        User.objects.get(username="test_user").delete()

    def test_status_and_column_name(self):
        client = Client()
        response = client.get(reverse('users'))
        self.assertEqual(200, response.status_code)
        self.assertIn(b"test_username", response.content)


class TestUserFormView(unittest.TestCase):

    def setUp(self):
        User.objects.create_user(first_name="test_first_name",
                                 username="test_user",
                                 password="test_password")

    def tearDown(self):
        User.objects.get(username="test_user").delete()

    def test_post(self):
        client = Client()
        client.post(reverse("users_create"),
                    data={"username": "test_user_post",
                          "password1": "test_user_post",
                          "password2": "test_user_post"}
                    )
        user = User.objects.get(username="test_user_post")
        self.assertEqual("test_user_post", user.username)

        User.objects.get(username="test_user_post").delete()

    def test_update_unauthorized(self):
        client = Client()

        user = User.objects.get(username="test_user")

        response = client.get(reverse("users_update",
                                      kwargs={"pk": user.id}))
            
        self.assertEqual(response.status_code, 302)

    def test_update_authorized(self):
        client = Client()

        client.login(username="test_user",
                     password="test_password")
        user = User.objects.get(username="test_user")
        response = client.get(reverse("users_update",
                                      kwargs={"pk": user.id}))

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"test_user", response.content)
        self.assertIn(b"test_first_name", response.content)

        client.post(reverse("logout"))

        response = client.get(reverse("users_update",
                                      kwargs={"pk": user.id}))
        self.assertEqual(response.status_code, 302)

    def test_delete(self):
        client = Client()

        User.objects.create_user(username="test_user_delete",
                                 password="test_delete")
        client.login(username="test_user_delete",
                     password="test_delete")
        user = User.objects.get(username="test_user_delete")

        client.post(reverse("users_delete",
                            kwargs={"pk": user.id}))

        self.assertFalse(
            User
            .objects
            .filter(username="test_user_delete").exists()
        )


if __name__ == '__main__':
    unittest.main()