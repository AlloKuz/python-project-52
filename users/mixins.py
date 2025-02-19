from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.shortcuts import redirect


class UserOnlyEditThemselfPermissionMixin(AccessMixin):
    fail_url = "/"
    fail_message = ""

    def dispatch(self, request, pk, *args, **kwargs):
        if request.user.id != pk:
            messages.error(request, self.fail_message)
            return redirect(self.fail_url)
        return super().dispatch(request, pk, *args, **kwargs)