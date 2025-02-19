from django.db import models

from django.utils.translation import gettext as _


class Status(models.Model):
    name = models.CharField(_("Имя"), max_length=32, unique=True)
    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Статус")
        verbose_name_plural = _("Статусы")