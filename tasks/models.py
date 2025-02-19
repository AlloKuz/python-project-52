from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

from statuses.models import Status


class Task(models.Model):
    name = models.CharField(_("Имя"), max_length=128, null=False)
    description = models.TextField(_("Описание"), blank=True)

    assigned_to = models.ForeignKey(verbose_name=_("Исполнитель"),
                                    to=User, on_delete=models.CASCADE,
                                    blank=True, null=True)
    status = models.ForeignKey(verbose_name=_("Статус"), to=Status,
                               on_delete=models.CASCADE)
    author = models.ForeignKey(verbose_name=_("Автор"), to=User,
                               on_delete=models.CASCADE,
                               related_name="author", blank=True, null=True)

    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Дата изменения"), auto_now=True)

    class Meta:
        verbose_name = _("Задача")
        verbose_name_plural = _("Задачи")

    def __str__(self):
        return self.name