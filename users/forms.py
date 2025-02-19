from django.contrib.auth.forms import UserCreationForm

from users.models import User


class UserForm(UserCreationForm):
    usable_password = None

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username",
                  "password1", "password2")