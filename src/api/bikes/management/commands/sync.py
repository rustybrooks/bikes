import datetime
import time

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from bikes.libs import stravaapi  # type: ignore
from bikes.models import StravaActivity  # type: ignore


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass
        # parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        while True:
            t1 = time.time()
            for user in User.objects.all():
                last_act = (
                    StravaActivity.objects.filter(user=user)
                    .order_by("-start_datetime")
                    .first()
                )
                last_date = (
                    last_act.start_datetime
                    if last_act
                    else datetime.datetime(2000, 1, 1)
                    # else datetime.datetime.now(datetime.timezone.utc)
                    # - datetime.timedelta(days=30)
                )

                print(f"Syncing {user.username} starting at {last_date}")

                activities = stravaapi.get_activities(
                    user, after=last_date - datetime.timedelta(days=1)
                )
                for act in activities:
                    StravaActivity.sync_one(user, act, full=True)

            diff = (60 * 5) - (time.time() - t1)
            print(f"sleeping {diff} seconds")
            time.sleep(diff)
