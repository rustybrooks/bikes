from django.contrib.auth.models import User
from django.db import models


class StravaTokens(models.Model):
    strava_token_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    auth_key = models.TextField(null=True)
