import logging

import numpy
from django.db import models  # type: ignore

logger = logging.getLogger(__name__)


class StravaPowerCurve(models.Model):
    power_curve_id = models.AutoField(primary_key=True)
    interval_length = models.IntegerField()
    watts = models.FloatField()
    activity = models.ForeignKey("StravaActivity", on_delete=models.DO_NOTHING)

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
        from bikes.models.strava_activity_stream import StravaActivityStream

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

        logger.info(
            "Processing power curve for %d (samples=%r)", activity_id, len(stream_data)
        )

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
        logger.info("segments = %r", len(segments))

        max_seconds = min(row[0] - first, 60 * 60 * 24)
        intervals = list(range(1, 10, 1))
        intervals.extend(range(10, 5 * 60, 10))
        intervals.extend(range(5 * 60, 15 * 60, 30))
        intervals.extend(range(15 * 60, 2 * 60 * 60, 60))
        intervals.extend(range(2 * 60 * 60, max_seconds, 60 * 10))

        power_objects = []
        for i, win in enumerate(intervals):
            # logger.info("interval=%r (%r/%r)", win, i + 1, len(intervals))
            val = max([cls.window(s, win) for s in segments])
            if val == 0:
                continue

            p = StravaPowerCurve(
                interval_length=win, watts=val, activity_id=activity_id
            )
            power_objects.append(p)

        StravaPowerCurve.objects.bulk_create(power_objects)
