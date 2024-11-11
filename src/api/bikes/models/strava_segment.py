from typing import Self, cast

from django.db import models  # type: ignore


class StravaSegment(models.Model):
    segment_id = models.BigIntegerField(primary_key=True)
    resource_state = models.IntegerField()
    name = models.TextField()
    activity_type = models.TextField()
    distance = models.FloatField()
    average_grade = models.FloatField()
    maximum_grade = models.FloatField()
    elevation_high = models.FloatField()
    elevation_low = models.FloatField()
    start_lat = models.FloatField(null=True)
    start_long = models.FloatField(null=True)
    end_lat = models.FloatField(null=True)
    end_long = models.FloatField(null=True)
    climb_category = models.IntegerField()
    city = models.TextField(null=True)
    state = models.TextField(null=True)
    country = models.TextField(null=True)
    private = models.BooleanField(default=False)
    starred = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
    total_elevation_gain = models.FloatField(null=True)
    # map... I dunno
    effort_count = models.IntegerField(null=True)
    athlete_count = models.IntegerField(null=True)
    hazardous = models.BooleanField(default=False)
    star_count = models.IntegerField(null=True)

    @classmethod
    def sync_one(cls, segment):
        segment_id = segment["id"]
        segs = StravaSegment.objects.filter(segment_id=segment_id)
        seg: Self = cast(
            Self, segs[0] if len(segs) else StravaSegment(segment_id=segment_id)
        )

        for key in [
            "resource_state",
            "name",
            "activity_type",
            "distance",
            "average_grade",
            "maximum_grade",
            "elevation_high",
            "elevation_low",
            "climb_category",
            "city",
            "state",
            "country",
            "private",
            "starred",
            "created_at",
            "updated_at",
            "total_elevation_gain",
            "effort_count",
            "athlete_count",
            "hazardous",
            "star_count",
        ]:
            # logger.warning("key = %r, val = %r", key, segment.get(key))
            setattr(seg, key, segment.get(key))

        seg.start_lat = segment["start_latlng"][0] if segment["start_latlng"] else None
        seg.start_long = segment["start_latlng"][1] if segment["start_latlng"] else None
        seg.end_lat = segment["end_latlng"][0] if segment["end_latlng"] else None
        seg.end_long = segment["end_latlng"][1] if segment["end_latlng"] else None

        seg.save()

        return seg
