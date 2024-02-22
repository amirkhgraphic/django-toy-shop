from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class MyBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False, blank=True)

    class Meta:
        ordering = ('-created_at',)
        abstract = True
