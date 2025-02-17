from django.forms import ModelForm

from statuses.models import Status


class StatusForm(ModelForm):
    class Meta:
        model = Status
        fields = ["name"]