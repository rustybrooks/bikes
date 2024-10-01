import logging

import numpy
from django.db import models  # type: ignore

from bikes.models.strava_activity import StravaActivity
from bikes.models.strava_activity_stream import StravaActivityStream

logger = logging.getLogger(__name__)


class StravaPowerCurve(models.Model):
    power_curve_id = models.AutoField(primary_key=True)
    interval_length = models.IntegerField()
    watts = models.FloatField()
    activity = models.ForeignKey(StravaActivity, on_delete=models.DO_NOTHING)

    @classmethod
    def window(cls, data, length):
        w = numpy.ones(length, "d")
        x = numpy.array([a[1] for a in data])

        if len(w) > len(x):
            return 0

        s = x
        y = numpy.convolve(w / w.sum(), s, mode="same")
        return max(y)

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

        last = None
        first: int
        stream_data = StravaActivityStream.objects.filter(
            activity_id=activity_id
        ).order_by("time")
        if not len(stream_data):
            logger.warning("No stream data for %d", activity_id)
            return

        logger.warning("Processing power curve for %d\n", activity_id)

        for dat in stream_data:
            row = (dat.time, dat.watts if dat.watts else 0)

            if last:
                diff = row[0] - last[0]

                if abs(diff) > 15:
                    segments.append(this_segment)
                    this_segment = []
                elif abs(diff) > 1:
                    for i in range(1, int(diff)):
                        this_segment.append((last[0] + i, last[1]))

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

            p = StravaPowerCurve()
            p.interval_length = win
            p.watts = val
            p.activity_id = activity_id
            # p.start_index = 0
            # p.end_index = 0
            p.save()
