import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

import bikes.models.strava_activity
from bikes import models


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass
        # parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for user in User.objects.all():
            first_act = bikes.models.strava_activity.StravaActivity.objects.filter(
                user=user
            ).order_by("start_datetime")[0]
            first_date = (
                first_act.start_datetime if first_act else datetime.datetime(2000, 1, 1)
            )
            bikes.models.strava_activity.StravaActivity.sync_many(
                user, first_date - datetime.timedelta(days=1)
            )
