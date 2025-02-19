from django.http import HttpResponse
from django.test import TestCase, Client
from django.urls import reverse

from task_manager.fixtures.load_fixture import load
from task_manager.users.models import User


class UsersTest(TestCase):
    fixtures = ["sample.json"]
    data = load("task_manager/fixtures/user_data.json")

    def setUp(self):
        self.client = Client(headers={"Accept-Language": "en"})
        self.user = User.objects.get(username=self.data["user"]["username"])

    def test_UserListView(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, HttpResponse.status_code)
        self.assertIn(b"Users", response.content)
        self.assertIn(self.user.username.encode(), response.content)

    def test_UserCreateView(self):
        response = self.client.post(reverse("users_create"),
                                    follow=True,
                                    data=self.data["new_user"])
        user = User.objects.get(username="new_test_user")
        self.assertEqual(self.data["new_user"]["username"], user.username)
        self.assertIn(b"User created", response.content)
        self.assertEqual(reverse("login"), response.request['PATH_INFO'])

    def test_UserUpdateView_get(self):
        url_for_update = reverse("users_update", kwargs={"pk": self.user.id})
        # unauthorized
        response = self.client.get(url_for_update, follow=True)
        self.assertIn(b"First you need to log in", response.content)
        self.assertRedirects(response,
                             reverse("login") + "?next=" + url_for_update)
        self.assertEqual(reverse("login"), response.request['PATH_INFO'])

        # authorized
        self.client.login(**self.data["user"])
        response = self.client.get(url_for_update)

        self.assertEqual(response.status_code, HttpResponse.status_code)
        self.assertIn(b"Edit user", response.content)
        self.assertIn(b"Username", response.content)
        self.assertIn(self.data["user"]["username"].encode(), response.content)

    def test_UserUpdateView_post(self):
        self.client.login(**self.data["user"])
        User.objects.create_user(**self.data["new_user_login"])
        new_user = User.objects.get(username=self.data["new_user"]["username"])

        # authenticated, not authorized
        # 'user_test' trying to update 'new_user_test'
        response = self.client.post(
            reverse("users_update", kwargs={"pk": new_user.id}),
            follow=True,
            data=self.data["new_user"]
        )
        self.assertIn(b"not allowed to edit another user", response.content)

        # authenticated, authorized
        response = self.client.post(
            reverse("users_update", kwargs={"pk": self.user.id}),
            follow=True,
            data=self.data["user_updated"],
        )

        self.assertEqual(response.status_code, HttpResponse.status_code)
        self.assertIn(b"User updated", response.content)
        self.assertEqual(
            User.objects.get(
                username=self.user.username
            ).first_name,
            "updated_test_user")

    def test_UserDeleteView(self):
        url_object = reverse("users_delete", kwargs={"pk": self.user.id})
        # unauthorized
        response = self.client.get(url_object, follow=True)
        self.assertIn(b"First you need to log in", response.content)
        self.assertRedirects(response, reverse("login") + "?next=" + url_object)
        self.assertEqual(reverse("login"), response.request['PATH_INFO'])

        # authorized, try to delete bounded
        self.client.login(**self.data["user"])
        response = self.client.post(url_object, follow=True)
        self.assertRedirects(response, reverse("users"))
        self.assertIn(b"Unable to delete user", response.content)
        self.client.logout()

        # create new unbounded user
        user = User.objects.create_user(**self.data["new_user_login"])
        self.client.login(**self.data["new_user_login"])

        # try to delete another user
        response = self.client.post(reverse("users_delete",
                                            kwargs={"pk": self.user.id}),
                                    follow=True)
        self.assertRedirects(response, reverse("users"))
        self.assertTrue(User.objects
                        .filter(username=self.data["new_user"]["username"])
                        .exists())
        self.assertIn(b"You are not allowed to delete another user",
                      response.content)

        # authorized to delete
        response = self.client.post(reverse("users_delete",
                                            kwargs={"pk": user.id}),
                                    follow=True)
        self.assertRedirects(response, reverse("users"))
        self.assertFalse(User.objects
                         .filter(username=self.data["new_user"]["username"])
                         .exists())
        self.assertIn(b"User deleted", response.content)