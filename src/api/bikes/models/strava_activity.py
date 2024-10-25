import logging

from django.contrib.auth.models import User
from django.db import models, transaction  # type: ignore

logger = logging.getLogger(__name__)


class StravaActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    activity_id = models.BigIntegerField(primary_key=True)
    external_id = models.TextField(null=True)
    upload_id = models.BigIntegerField(null=True)
    athlete_id = models.BigIntegerField()
    activity_name = models.TextField(null=True)
    distance = models.FloatField()
    moving_time = models.IntegerField()
    elapsed_time = models.IntegerField()
    total_elevation_gain = models.FloatField()
    elev_high = models.FloatField(null=True)
    elev_low = models.FloatField(null=True)
    type = models.TextField()
    start_datetime = models.DateTimeField(null=True)
    start_datetime_local = models.DateTimeField()
    timezone = models.TextField()
    start_lat = models.FloatField(null=True)
    start_long = models.FloatField(null=True)
    end_lat = models.FloatField(null=True)
    end_long = models.FloatField(null=True)
    achievement_count = models.IntegerField()
    athlete_count = models.IntegerField()
    # map # I dunno
    trainer = models.BooleanField(default=False)
    commute = models.BooleanField(default=False)
    manual = models.BooleanField(default=False)
    private = models.BooleanField(default=False)
    embed_token = models.TextField(null=True)
    flagged = models.BooleanField(default=False)
    workout_type = models.IntegerField(null=True)
    gear_id = models.TextField(null=True)
    average_speed = models.FloatField(null=True)
    max_speed = models.FloatField(null=True)
    average_cadence = models.FloatField(null=True)
    average_temp = models.FloatField(null=True)
    average_watts = models.FloatField(null=True)
    max_watts = models.FloatField(null=True)
    weighted_average_watts = models.FloatField(null=True)
    kilojoules = models.FloatField(null=True)
    device_watts = models.BooleanField(default=False, null=True)
    average_heartrate = models.FloatField(null=True)
    max_heartrate = models.FloatField(null=True)
    suffer_score = models.IntegerField(null=True)

    def json(self):
        return {
            "user_id": self.user.id,
            "start_datetime_local": self.start_datetime_local,
            "activity_id": self.activity_id,
            "activity_name": self.activity_name,
            "distance_miles": self.distance_miles(),
            "moving_time": self.moving_time,
            "total_elevation_gain_feet": self.total_elevation_gain_feet(),
            "average_watts": self.average_watts,
            "average_heartrate": self.average_heartrate,
            "suffer_score": self.suffer_score,
        }

    def average_speed_miles(self):
        return self.distance_miles() / (self.moving_time / 3600.0)

    def distance_miles(self):
        return self.distance / 1609.34

    def total_elevation_gain_feet(self):
        return self.total_elevation_gain * 3.28084

    @classmethod
    def time_formatted(cls, sec):
        hours = sec / 3600
        minutes = (sec % 3600) / 60
        seconds = sec % 60
        return "%2d:%02d:%02d" % (hours, minutes, seconds)

    def moving_time_formatted(self):
        return self.time_formatted(self.moving_time)

    def elapsed_time_formatted(self):
        return self.time_formatted(self.elapsed_time)

    # @classmethod
    # def sync_one_byobj(cls, user, activity):
    #     data = stravaapi.get_activity(user, activity.activity_id)
    #     cls.sync_one(user, data, full=True, rebuild=True)

    @classmethod
    @transaction.atomic
    def sync_one(cls, user, activity, full=False, rebuild=False):
        from bikes.libs import stravaapi
        from bikes.models import (
            StravaActivitySegmentEffort,
            StravaActivityStream,
            StravaSpeedCurve,  # type: ignore
        )

        activity_id = activity["id"]
        actlist = cls.objects.filter(activity_id=activity_id)

        # If we already have this one, let's not resync
        if len(actlist) and not rebuild:
            return

        if "segment_efforts" not in activity and full:
            return cls.sync_one(user, stravaapi.get_activity(user, activity["id"]))

        logger.info(
            f"Syncing strava activity id={activity['id']} start={activity['start_date']}"
        )

        if len(actlist):
            act = actlist[0]
        else:
            act = StravaActivity()
            act.activity_id = activity_id
            act.user = user

        for key in [
            "external_id",
            "upload_id",
            "distance",
            "moving_time",
            "elapsed_time",
            "total_elevation_gain",
            "elev_high",
            "elev_low",
            "type",
            "timezone",
            "achievement_count",
            "athlete_count",
            "trainer",
            "commute",
            "manual",
            "private",
            "embed_token",
            "workout_type",
            "gear_id",
            "average_speed",
            "max_speed",
            "average_cadence",
            "average_temp",
            "average_watts",
            "max_watts",
            "weighted_average_watts",
            "kilojoules",
            "device_watts",
            "average_heartrate",
            "max_heartrate",
            "suffer_score",
            "flagged",
        ]:
            setattr(act, key, activity.get(key))

        act.athlete_id = activity["athlete"]["id"]

        act.activity_name = activity["name"]
        act.start_datetime = activity["start_date"]
        act.start_datetime_local = activity["start_date_local"]

        act.start_lat = (
            activity["start_latlng"][0] if activity["start_latlng"] else None
        )
        act.start_long = (
            activity["start_latlng"][1] if activity["start_latlng"] else None
        )
        act.end_lat = activity["end_latlng"][0] if activity["end_latlng"] else None
        act.end_long = activity["end_latlng"][1] if activity["end_latlng"] else None

        act.save()

        if "segment_efforts" in activity:
            for e in activity.get("segment_efforts", []):
                _effort = StravaActivitySegmentEffort.sync_one(act, e)

                # if new:
                #     StravaSegmentHistory.sync_one(
                #         user, effort.segment_id, act.athlete_id
                #     )

        StravaActivityStream.sync(user, act)

        return act

    # @classmethod
    # def sync_many(cls, user, first_date=None):
    #     first_date = first_date or (tznow() - datetime.timedelta(days=14))
    #
    #     activities = stravaapi.get_activities(user, after=first_date)
    #     for act in activities:
    #         cls.sync_one(user, act, full=True)

    # @classmethod
    # def update_incomplete(cls, user):
    #     incomplete = cls.objects.filter(embed_token__isnull=True)
    #
    #     updated = 0
    #     for activity in incomplete:
    #         updated += 1
    #         cls.sync_one(user, stravaapi.get_activity(user, activity.activity_id))
    #
    #     incomplete = cls.objects.filter(embed_token__isnull=True)
    #
    #     return updated, len(incomplete)

    # @classmethod
    # def update_streams(cls, user):
    #     all = cls.objects.filter()
    #
    #     updated = 0
    #     for activity in all:
    #         streams = StravaActivityStream.objects.filter(activity=activity)
    #         if len(streams):
    #             continue
    #
    #         logger.warning("Updating stream for %d\n", activity.activity_id)
    #         try:
    #             cls.sync_one(user, stravaapi.get_activity(user, activity.activity_id))
    #         except stravaapi.StravaError as e:
    #             logger.error(
    #                 "Error updating stream for %r: %r", activity.activity_id, e
    #             )
    #             continue
    #
    #         updated += 1
    #
    #         if updated >= 100:
    #             break
    #
    #     return updated

    @classmethod
    def update_curves(cls):
        from bikes.models import (
            StravaPowerCurve,
            StravaSpeedCurve,  # type: ignore
        )

        all = cls.objects.filter()

        updated = 0
        for activity in all:
            streams1 = StravaPowerCurve.objects.filter(activity=activity)
            streams2 = StravaSpeedCurve.objects.filter(activity=activity)
            if len(streams1) and len(streams2):
                continue

            if not len(streams1):
                StravaPowerCurve.process_curve(activity.activity_id)

            if not len(streams2):
                StravaSpeedCurve.process_curve(activity.activity_id)

        updated += 1

        #            if updated >= 10:
        #                break

        return updated

    def __unicode__(self):
        return "Strava Activity: %s (%0.1f hours)" % (
            self.start_datetime_local,
            self.moving_time / (60.0 * 60),
        )
