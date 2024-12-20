import logging

import numpy
from django.db import models  # type: ignore

logger = logging.getLogger(__name__)


class StravaSpeedCurve(models.Model):
    speed_curve_id = models.AutoField(primary_key=True)
    interval_length = models.IntegerField()
    speed = models.FloatField()
    activity = models.ForeignKey("StravaActivity", on_delete=models.DO_NOTHING)

    @property
    def speed_mph(self):
        return (self.speed / 1609.34) * 3600

    @classmethod
    def window(cls, data, length):
        if length >= len(data):
            return 0

        x = numpy.array([a[2] for a in data], dtype=float)
        tm = numpy.array([a[0] for a in data], dtype=float)
        distw = x[length:] - x[:-length]
        tmw = tm[length:] - tm[:-length]
        # speed = distw / tmw
        speed = numpy.divide(distw, tmw, out=numpy.zeros_like(distw), where=tmw != 0)

        return max(speed)

    @classmethod
    def process_curve(cls, activity_id, delete=False):
        from bikes.models.strava_activity_stream import StravaActivityStream  # type: ignore

        existing = cls.objects.filter(activity_id=activity_id)
        if len(existing):
            if delete:
                existing.delete()
            else:
                return

        segments = []
        this_segment: list[tuple] = []

        stream_data = StravaActivityStream.objects.filter(
            activity_id=activity_id
        ).order_by("time")
        if not len(stream_data):
            logger.warning("No stream data for %d", activity_id)
            return

        logger.info("Processing speed curve for %d", activity_id)

        last = None
        first: int
        for dat in stream_data:
            row = (
                dat.time,
                dat.velocity_smooth if dat.velocity_smooth else 0,
                dat.distance if dat.distance else 0,
            )

            if last:
                diff = row[0] - last[0]

                if abs(diff) > 15:
                    segments.append(this_segment)
                    this_segment = []
                elif abs(diff) > 1:
                    for i in range(1, int(diff)):
                        this_segment.append((last[0] + i, last[1], last[2]))

                this_segment.append(row)
            else:
                first = row[0]

            last = row

        segments.append(this_segment)

        max_seconds = min(row[0] - first, 60 * 60 * 24)
        intervals = list(range(1, 10, 1))
        intervals.extend(range(10, 5 * 60, 10))
        intervals.extend(range(5 * 60, 15 * 60, 30))
        intervals.extend(range(15 * 60, 2 * 60 * 60, 60))
        intervals.extend(range(2 * 60 * 60, max_seconds, 60 * 10))

        speed_objects = []
        for win in intervals:
            val = max([cls.window(s, win) for s in segments])

            if val == 0:
                continue

            s = StravaSpeedCurve(
                interval_length=win, speed=val, activity_id=activity_id
            )
            speed_objects.append(s)

        StravaSpeedCurve.objects.bulk_create(speed_objects)
