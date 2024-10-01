from django.db import models

from bikes.models import StravaActivity, StravaSegment


class StravaSegmentHistorySummary(models.Model):
    segment_history_summary_id = models.AutoField(primary_key=True)
    segment = models.ForeignKey(StravaSegment, on_delete=models.DO_NOTHING)
    activity = models.ForeignKey(StravaActivity, on_delete=models.DO_NOTHING)
