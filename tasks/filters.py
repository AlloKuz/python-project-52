import django_filters

from django.forms.widgets import CheckboxInput
from django.utils.translation import gettext_lazy as _

from tasks.models import Task
from labels.models import Label


class TasksFilter(django_filters.FilterSet):
    author = django_filters.BooleanFilter(method="is_author",
                                          widget=CheckboxInput(),
                                          field_name="author",
                                          label=_("Is author"))
    labels = django_filters.ModelChoiceFilter(queryset=Label.objects,
                                              label="Label")

    class Meta:
        model = Task
        fields = ["status", "executor", "labels"]

    def is_author(self, queryset, name, value):
        author = getattr(self.request, 'user', None)
        if value:
            return queryset.filter(author=author)
        return queryset