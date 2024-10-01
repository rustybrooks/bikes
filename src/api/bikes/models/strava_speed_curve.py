import logging

import numpy
from django.db import models  # type: ignore

from bikes.models import StravaActivity, StravaActivityStream  # type: ignore

logger = logging.getLogger(__name__)


class StravaSpeedCurve(models.Model):
    speed_curve_id = models.AutoField(primary_key=True)
    interval_length = models.IntegerField()
    speed = models.FloatField()
    activity = models.ForeignKey(StravaActivity, on_delete=models.DO_NOTHING)

    @property
    def speed_mph(self):
        return (self.speed / 1609.34) * 3600

    @classmethod
    def window(cls, data, length):
        if length >= len(data):
            return 0

        x = numpy.array([a[2] for a in data])
        tm = numpy.array([a[0] for a in data])
        distw = x[length:] - x[:-length]
        tmw = tm[length:] - tm[:-length]
        speed = distw / tmw
        return max(speed)

    @classmethod
    def process_curve(cls, activity_id, delete=False):
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

        logger.warning("Processing power curve for %d\n", activity_id)

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

        max_seconds = row[0] - first
        intervals = list(range(1, 10, 1))
        intervals.extend(range(10, 5 * 60, 10))
        intervals.extend(range(5 * 60, 15 * 60, 30))
        intervals.extend(range(15 * 60, max_seconds, 60))

        for win in intervals:
            val = max([cls.window(s, win) for s in segments])

            if val == 0:
                continue

            #            logger.warning("Adding point %r", (activity_id_, interval_length, val)
            s = StravaSpeedCurve()
            s.interval_length = win
            s.speed = val
            s.activity_id = activity_id
            # s.start_index = 0
            # s.end_index = 0
            s.save()
