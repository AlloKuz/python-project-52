from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import LoginView, LogoutView


class LoginUserView(SuccessMessageMixin, LoginView):
    success_message = _("You logged in")
    template_name = "form.html"
    form_class = AuthenticationForm
    next_page = "/"
    redirect_authenticated_user = True
    extra_context = {
        'page_header': _('Login'),
        'button_text': _('Enter'),
    }


class LogoutUserView(LogoutView):
    next_page = "/"

    def post(self, request, *args, **kwargs):
        messages.success(request, _("You logged out"))
        return super().post(request, *args, **kwargs)