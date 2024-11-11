import datetime
import logging
from typing import Any
from urllib.parse import urlencode

from django.db import models  # type: ignore
from django.urls import reverse  # type: ignore

from bikes import plans

logger = logging.getLogger(__name__)

tpmap = {
    "CTB": plans.CTBv1,
    "TCC": plans.TCC,
}


def tp_from_season(s):
    return tpmap[s.training_plan](s.params)


class TrainingWeek(models.Model):
    week_start_date = models.DateField()
    season = models.ForeignKey(
        "Season",
        unique_for_date="week_start_date",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    week_type = models.CharField(max_length=50)  # , choices=WEEK_TYPE_CHOICES
    week_type_num = models.IntegerField()

    def __unicode__(self):
        return "%s:%s-%s" % (self.week_start_date, self.week_type, self.week_type_num)

    def json(self, cal):
        output: dict[str, Any] = {"entries": []}
        for elist in cal.entries_by_week(self):
            output["entries"].append([e.json() for e in elist])

        for el in ("week_type",):
            output[el] = getattr(self, el)

        output["week_start_date"] = self.week_start_date

        return output

    def races(self, race_filter=None):
        from bikes.models import Race

        if race_filter is None:
            race_filter = Race.objects.filter(season=self.season)

        f = race_filter.select_related("week").filter(
            race_date__gte=self.week_start_date
        )
        f = f.filter(race_date__lt=self.week_start_date + datetime.timedelta(days=7))

        return f

    def weekly_hours(self):
        logger.warning("tp_from_season... %r", self.week_start_date)
        tp = tp_from_season(self.season)
        return tp.weekly_hours(self)

    def entries(self, populate=False):
        if populate:
            self.populate_entries(delete_first=True)

        m: dict[int, Any] = {}
        for d in range(7):
            m[d] = []
        for entry in TrainingEntry.objects.select_related("week").filter(week=self):
            diff = (entry.entry_date - self.week_start_date).days
            m[diff].append(entry)

        return m.values()

    def populate_entries(self, delete_first=False, save=True):
        entry_by_orig = {}
        if save:
            if delete_first:
                TrainingEntry.objects.filter(week=self).delete()
            else:
                saved_entries = TrainingEntry.objects.filter(week=self)
                for entry in saved_entries:
                    entry_by_orig[entry.scheduled_dow] = entry

        tp = tp_from_season(self.season)
        entries = []
        for e in tp.plan_entries(self):
            dow = e.pop("dow")
            if dow in entry_by_orig:
                continue
            e["season"] = self.season
            e["week"] = self
            e["entry_date"] = self.week_start_date + datetime.timedelta(days=dow)
            entries.append(TrainingEntry(**e))

        if save:
            TrainingEntry.objects.bulk_create(entries)

        return entries

    def is_this_week(self):
        today = datetime.date.today()
        return (
            self.week_start_date
            <= today
            < self.week_start_date + datetime.timedelta(days=7)
        )


class TrainingEntry(models.Model):
    entry_date = models.DateField()
    season = models.ForeignKey(
        "Season", unique_for_date="entry_date", on_delete=models.DO_NOTHING
    )
    week = models.ForeignKey(TrainingWeek, on_delete=models.DO_NOTHING)
    workout_type = models.CharField(max_length=50)
    activity_type = models.CharField(max_length=50)
    scheduled_dow = models.IntegerField()
    scheduled_length = models.FloatField()
    scheduled_length2 = models.FloatField()
    actual_length = models.FloatField()
    notes = models.CharField(max_length=2000)

    def __unicode__(self):
        return "%s" % (self.entry_date,)

    def workout_type_list(self):
        tp = tp_from_season(self.season)
        return tp.workout_types(self)

    def link(self, workout_type):
        if self.workout_type == workout_type:
            return "<b>%s</b>" % workout_type
        else:
            wt = workout_type

            url = "<a href='%s?%s'>%s</a>" % (
                reverse("update_entry", kwargs={"entry_id": self.pk}),
                urlencode({"workout_type": workout_type}),
                wt,
            )
            return url

    def is_today(self):
        return datetime.date.today() == self.entry_date

    def workout_description(self, wo_type):
        tp = tp_from_season(self.season)
        return tp.workout_description(wo_type)
