from django.db import models  # type: ignore

from bikes.models.strava_activity import StravaActivity  # type: ignore
from bikes.models.strava_segment import StravaSegment  # type: ignore


class StravaActivitySegmentEffort(models.Model):
    activity_segment_id = models.BigIntegerField(primary_key=True)
    activity = models.ForeignKey(StravaActivity, on_delete=models.DO_NOTHING)
    resource_state = models.IntegerField()
    name = models.TextField()
    elapsed_time = models.IntegerField()
    moving_time = models.IntegerField()
    start_datetime = models.DateTimeField()
    start_datetime_local = models.DateTimeField()
    distance = models.FloatField()
    start_index = models.BigIntegerField()
    end_index = models.BigIntegerField()
    average_cadence = models.FloatField(null=True)
    average_watts = models.FloatField(null=True)
    device_watts = models.BooleanField(default=False, null=True)
    average_heartrate = models.FloatField(null=True)
    max_heartrate = models.FloatField(null=True)
    segment = models.ForeignKey(StravaSegment, on_delete=models.DO_NOTHING)
    kom_rank = models.IntegerField(null=True)
    pr_rank = models.IntegerField(null=True)
    hidden = models.BooleanField(default=False)

    # @classmethod
    # def sync_one(cls, activity, segment):
    #     id = segment["id"]
    #     segs = cls.objects.filter(activity_segment_id=id)
    #     if len(segs):
    #         sege = segs[0]
    #     else:
    #         sege = StravaActivitySegmentEffort()
    #         sege.activity_segment_id = id
    #
    #     sege.activity = activity
    #     sege.start_datetime = segment.get("start_date")
    #     sege.start_datetime_local = segment.get("start_date_local")
    #
    #     for key in [
    #         "resource_state",
    #         "name",
    #         "elapsed_time",
    #         "moving_time",
    #         "distance",
    #         "start_index",
    #         "end_index",
    #         "average_cadence",
    #         "average_watts",
    #         "device_watts",
    #         "average_heartrate",
    #         "max_heartrate",
    #         "kom_rank",
    #         "pr_rank",
    #         "hidden",
    #     ]:
    #         # logger.warning("key = %r, val = %r", key, segment.get(key))
    #         setattr(sege, key, segment.get(key))
    #
    #     sege.segment = StravaSegment.sync_one(segment["segment"])
    #
    #     sege.save()
    #
    #     StravaActivitySegmentEffortAch.sync(sege, segment["achievements"])
    #
    #     return sege


class StravaActivitySegmentEffortAch(models.Model):
    achievement_id = models.AutoField(primary_key=True)
    segment_effort = models.ForeignKey(
        StravaActivitySegmentEffort, on_delete=models.DO_NOTHING
    )
    type_id = models.IntegerField()
    type = models.TextField()
    rank = models.IntegerField()

    # @classmethod
    # def sync(cls, segment_effort, achievements):
    #     # logger.warning("ach = %r", achievements)
    #     if not len(achievements):
    #         return
    #
    #     cls.objects.filter(segment_effort=segment_effort).delete()
    #     for ach in achievements:
    #         a = StravaActivitySegmentEffortAch()
    #         a.segment_effort = segment_effort
    #         a.type_id = ach["type_id"]
    #         a.type = ach["type"]
    #         a.rank = ach["rank"]
    #
    #         a.save()
