from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import MinimumLengthValidator
from django.utils.translation import gettext as _

from task_manager.settings import AUTH_PASSWORD_VALIDATORS

class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username")


class UserUpdateForm(forms.ModelForm):
    password = forms.CharField(
        label=_("Пароль"),
        widget=forms.PasswordInput(),
    )
    confirm_password = forms.CharField(
        label=_("Подтверждение пароля"),
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if len(password) < 3:
            self.add_error('password', _('Пароль должен быть больше 3 символов'))

        if password != confirm_password:
            self.add_error('confirm_password', _("Пароли не совпадают"))

        return cleaned_data
