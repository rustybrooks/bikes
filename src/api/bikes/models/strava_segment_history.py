import datetime
import logging

from django.db import models  # type: ignore

from bikes.libs import stravaapi
from bikes.models.strava_activity import StravaActivity
from bikes.models.strava_segment import StravaSegment
from bikes.models.strava_segment_history_summary import StravaSegmentHistorySummary  # type: ignore

logger = logging.getLogger(__name__)


class StravaSegmentHistory(models.Model):
    segment_history_id = models.AutoField(primary_key=True)
    segment = models.ForeignKey(StravaSegment, on_delete=models.DO_NOTHING)
    activity = models.ForeignKey(StravaActivity, on_delete=models.DO_NOTHING)
    recorded_datetime = models.DateTimeField()
    rank = models.IntegerField()
    entries = models.IntegerField()
    average_hr = models.FloatField(null=True)
    average_watts = models.FloatField(null=True)
    distance = models.FloatField(null=True)
    elapsed_time = models.IntegerField()
    moving_time = models.IntegerField()

    @classmethod
    def sync_one(cls, user, segment_id, athlete_id):
        try:
            leaderboard = stravaapi.get_segment_leaderboard(user, segment_id)
        except stravaapi.StravaError:
            logger.warning(
                "Failed to fetch segment leaderboard for segment id %d", segment_id
            )
            return

        # get current best and don't write if it's not better?

        logger.info("Syncing %r", segment_id)
        for el in leaderboard["entries"]:
            if el["athlete_id"] == athlete_id:
                # is this the same information we already had?
                existing = StravaSegmentHistorySummary.objects.filter(
                    segment_id=segment_id
                )
                if (
                    len(existing)
                    and existing[0].activity.activity_id == el["activity_id"]
                ):
                    break

                x = StravaSegmentHistory()
                x.segment_id = segment_id
                x.entries = leaderboard["entry_count"]
                x.activity_id = el["activity_id"]
                x.recorded_datetime = datetime.datetime.now(tz=datetime.timezone.utc)
                for key in [
                    "rank",
                    "average_hr",
                    "average_watts",
                    "distance",
                    "elapsed_time",
                    "moving_time",
                ]:
                    setattr(x, key, el[key])

                x.save()

                y = StravaSegmentHistorySummary()
                y.segment_id = segment_id
                y.activity_id = el["activity_id"]
                y.save()

                break

    @classmethod
    def sync_all(cls, user, athlete_id):
        import time

        segments = StravaSegment.objects.filter()
        for s in segments:
            try:
                cls.sync_one(user, s.segment_id, athlete_id)
                time.sleep(2)
            except stravaapi.StravaError:
                logger.error("Error while syncing segment %r", s.segment_id)
