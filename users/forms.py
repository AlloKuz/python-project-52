from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class UserCreateForm(UserCreationForm):
    usable_password = None

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username")


class UserUpdateForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(),
    )
    password2 = forms.CharField(
        label=_("Confirm password"),
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("password2")

        if len(password) < 3:
            self.add_error('password1',
                           _('Password should be at least 3 symbols'))

        if password != confirm_password:
            self.add_error('password2',
                           _("Passwords doesn't match"))

        return cleaned_data