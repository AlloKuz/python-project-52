from django.db import models
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    name = models.CharField(_("Name"),
                            max_length=64,
                            unique=True)
    created_at = models.DateTimeField(_("Created at"),
                                      auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Label")
        verbose_name_plural = _("Labels")
