from django.test import TestCase, Client
from django.urls import reverse

from task_manager.users.models import User


class UsersTest(TestCase):
    fixtures = ["sample.json"]

    def setUp(self):
        self.client = Client(headers={"Accept-Language": "en"})
        self.user = User.objects.get(username="test_user")

    def test_UserListView(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(200, response.status_code)
        self.assertIn(b"Users", response.content)
        self.assertIn(b"test_user", response.content)

    def test_UserCreateView(self):
        response = self.client.post(reverse("users_create"),
                                    follow=True,
                                    data={"username": "test_user_post",
                                          "password1": "test_user_post",
                                          "password2": "test_user_post"})
        user = User.objects.get(username="test_user_post")
        self.assertEqual("test_user_post", user.username)
        self.assertIn(b"User created", response.content)
        self.assertEqual(reverse("login"), response.request['PATH_INFO'])

    def test_UserUpdateView(self):
        url_for_update = reverse("users_update", kwargs={"pk": self.user.id})
        # unauthorized
        response = self.client.get(url_for_update, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"First you need to log in", response.content)
        self.assertEqual(reverse("login"), response.request['PATH_INFO'])

        # authorized
        self.client.login(username="test_user", password="test_password")
        response = self.client.get(url_for_update)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Edit user", response.content)
        self.assertIn(b"Username", response.content)
        self.assertIn(b"test_user", response.content)

        # POST
        response = self.client.post(
            url_for_update,
            follow=True,
            data={
                "username": "test_user",
                "first_name": "First_name",
                "password1": "test_password",
                "password2": "test_password",
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"User updated", response.content)
        self.assertEqual(User.objects.get(username="test_user").first_name,
                         "First_name")

    def test_UserDeleteView(self):
        url_object = reverse("users_delete", kwargs={"pk": self.user.id})
        # unauthorized
        response = self.client.get(url_object, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"First you need to log in", response.content)
        self.assertEqual(reverse("login"), response.request['PATH_INFO'])

        # authorized, try to delete bounded
        self.client.login(username="test_user", password="test_password")
        response = self.client.post(url_object, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Unable to delete user", response.content)
        self.client.logout()

        # create new unbounded user
        user = User.objects.create_user(username="test_user_delete",
                                        password="test_password_delete")
        self.client.login(username="test_user_delete",
                          password="test_password_delete")

        response = self.client.post(reverse("users_delete",
                                            kwargs={"pk": user.id}),
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects
                         .filter(username="test_user_delete").exists())
        self.assertIn(b"User deleted", response.content)