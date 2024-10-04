import datetime
import logging
from typing import Any
from urllib.parse import urlencode

from django.db import models  # type: ignore
from django.urls import reverse  # type: ignore

# from bikes import plans  # type: ignore

logger = logging.getLogger(__name__)

# tpmap = {
#     "CTB": plans.CTB,
#     "TCC": plans.TCC,
# }


def tp_from_season(s):
    # logger.error(
    #     "tp_from_season - season = %r, params = %r, tp = %r",
    #     s,
    #     s.params,
    #     s.training_plan,
    # )
    # return tpmap[s.training_plan](json.loads(s.params))
    return []


class TrainingWeek(models.Model):
    # WEEK_TYPE_CHOICES = (
    #     ('Prep', 'Prep'),
    #     ('Base 1', 'Base 1'),
    #     ('Base 2', 'Base 2'),
    #     ('Base 3', 'Base 3'),
    #     ('Build 1', 'Build 1'),
    #     ('Build 2', 'Build 2'),
    #     ('Peak', 'Peak'),
    #     ('RaceSat', 'Race Saturday'),
    #     ('RaceSun', 'Race Sunday'),
    #     ('RaceSatSun', 'Race Saturday and Sunday'),
    #     ('Transition', 'Transition'),
    # )

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
        output: dict[str, Any] = {}
        output["entries"] = []
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

    def populate_entries(self, delete_first=False):
        entry_by_orig = {}
        if delete_first:
            TrainingEntry.objects.filter(week=self).delete()
        else:
            saved_entries = TrainingEntry.objects.filter(week=self)
            for entry in saved_entries:
                entry_by_orig[entry.scheduled_dow] = entry

        tp = tp_from_season(self.season)
        for e in tp.plan_entries(self):
            dow = e.pop("dow")
            if dow in entry_by_orig:
                continue
            e["season"] = self.season
            e["week"] = self
            e["entry_date"] = self.week_start_date + datetime.timedelta(days=dow)
            entry = TrainingEntry(**e)
            entry.save()

    def is_this_week(self):
        today = datetime.date.today()
        return (
            self.week_start_date <= today
            and today < self.week_start_date + datetime.timedelta(days=7)
        )


class TrainingEntry(models.Model):
    # NAME_CHOICES = (
    #     ('E1', 'Recovery'),
    #     ('E2', 'Aerobic'),
    #     ('E3', 'Fixed Gear'),
    #     ('F1', 'Moderate Hills'),
    #     ('F2', 'Long Hills'),
    #     ('F3', 'Steep Hills'),
    #     ('S1', 'Spin-ups'),
    #     ('S2', 'Isolated Leg'),
    #     ('S3', 'Cornering'),
    #     ('S4', 'Bumping'),
    #     ('S5', 'Form Sprints'),
    #     ('S6', 'Sprints'),
    #     ('M1', 'Tempo'),
    #     ('M2', 'Cruise Intervals'),
    #     ('M3', 'Hill Cruise Intervals'),
    #     ('M4', 'Motorpaced Cruise Intervals'),
    #     ('M5', 'Criss-Cross Threshold'),
    #     ('M6', 'Threshold'),
    #     ('M7', 'Motorpaced Threshold'),
    #     ('A1', 'Group Ride'),
    #     ('A2', 'SE Intervals'),
    #     ('A3', 'Pyramid Intervals'),
    #     ('A4', 'Hill Intervals'),
    #     ('A5', 'Lactate Tolerance Reps'),
    #     ('A6', 'Hill Reps'),
    #     ('P1', 'Jumps'),
    #     ('P2', 'Hill Sprints'),
    #     ('P3', 'Crit Sprints'),
    #     ('T1', 'Aerobic Time Trial'),
    #     ('T2', 'Time Trial'),
    #     ('RACE', 'Race'),
    #     ('OFF', 'Off'),
    #     )

    entry_date = models.DateField()
    season = models.ForeignKey(
        "Season", unique_for_date="entry_date", on_delete=models.DO_NOTHING
    )
    week = models.ForeignKey(TrainingWeek, on_delete=models.DO_NOTHING)
    workout_type = models.CharField(max_length=50)  # , choices=NAME_CHOICES
    scheduled_dow = models.IntegerField()
    scheduled_length = models.FloatField()
    scheduled_length2 = models.FloatField()
    actual_length = models.FloatField()
    notes = models.CharField(max_length=2000)

    def __unicode__(self):
        return "%s" % (self.entry_date,)

    def json(self):
        output = {}

        for el in (
            "id",
            "entry_date",
            "workout_type",
            "scheduled_dow",
            "scheduled_length",
            "actual_length",
        ):
            output[el] = getattr(self, el)

        output["workout_types"] = self.workout_type_list()

        return output

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
