from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User
from statuses.models import Status
from labels.models import Label


class Task(models.Model):
    name = models.CharField(_("Name"), max_length=128, null=False)
    description = models.TextField(_("Description"), blank=True)

    executor = models.ForeignKey(verbose_name=_("Executor"),
                                 to=User, on_delete=models.PROTECT,
                                 blank=True, null=True)
    status = models.ForeignKey(verbose_name=_("Status"), to=Status,
                               on_delete=models.PROTECT)
    author = models.ForeignKey(verbose_name=_("Author"), to=User,
                               on_delete=models.PROTECT,
                               related_name="author", blank=True, null=True)

    labels = models.ManyToManyField(verbose_name=_("Labels"),
                                    to=Label,
                                    blank=True)

    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")

    def __str__(self):
        return self.name