from django.contrib.auth.models import User  # type: ignore
from django.db import models  # type: ignore


class StravaToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    access_token = models.TextField(null=True)
    refresh_token = models.TextField(null=True)
    expires_at = models.DateTimeField(null=True)
