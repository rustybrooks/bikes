import datetime
import logging
import time

import django.db
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from bikes.libs import stravaapi  # type: ignore
from bikes.models import StravaActivity  # type: ignore

logger = logging.getLogger(__name__)


# interval = (60 * 10)
interval = 60 * 60 * 24


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass
        # parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        outcomes = []

        while True:
            try:
                t1 = time.time()
                django.db.close_old_connections()
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
                    )
                    last_date = datetime.datetime(2010, 1, 1)
                    print(f"Syncing {user.username} starting at {last_date}")

                    try:
                        activities = stravaapi.get_activities(
                            user, after=last_date - datetime.timedelta(days=1)
                        )
                        for act in activities:
                            StravaActivity.sync_one(user, act, full=True)
                    except Exception:
                        logger.exception("Failed to retrieve activities")

                took = time.time() - t1
                diff = interval - took
                print(f"sleeping {diff:0.1f} seconds (took {took:0.1f} seconds)")
                outcomes.append(0)
                time.sleep(diff)
            except Exception:
                logger.exception("Error while handling users")

                outcomes.append(1)
                if sum(outcomes[-10:]) >= 10:
                    logger.error("10 exceptions in a row, bailing")
                    break

                time.sleep(30)

            outcomes = outcomes[-10:]
