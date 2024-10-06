from django.contrib.auth.models import User
from django.db import models


class Season(models.Model):
    # LIMIT_FACTOR_CHOICES = (
    #     ('Strength', 'Strength'),
    #     ('Speed', 'Speed'),
    #     ('Muscualar-Endurance', 'Muscualar-Endurance'),
    #     ('Speed-Endurance', 'Speed-Endurance'),
    #     ('Power', 'Power'),
    # )

    TP_CHOICES = (
        ("CTB", "Cyclist's Training Bible"),
        ("TCC", "Time Crunched Cyclist"),
    )

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # limiting_factors_1 = models.CharField(max_length=50, choices=LIMIT_FACTOR_CHOICES)
    # limiting_factors_2 = models.CharField(max_length=50, choices=LIMIT_FACTOR_CHOICES)
    training_plan = models.CharField(max_length=100, choices=TP_CHOICES)
    season_start_date = models.DateField()
    season_end_date = models.DateField()
    # annual_hours = models.IntegerField()
    params = models.JSONField(max_length=5000)

    # ftp_hr = 170  This is what I got from Rubber Glove last year but holy crap
    ftp_hr = 163
    ftp_watts = 215

    def zone_hr(self, zone):
        zones = {
            "": 0,
            "1": 0.81,
            "2": 0.89,
            "3": 0.93,
            "4": 0.99,
            "5a": 1.02,
            "5b": 1.06,
            "5c": 1.10,
            "6": 1.10,
        }

        return int(self.ftp_hr * zones[zone])

    def zone_power(self, zone):
        zones = {
            "": 0,
            "1": 0.55,
            "2": 0.74,
            "3": 0.89,
            "4": 1.04,
            "5a": 1.12,
            "5b": 1.17,
            "5c": 1.2,
            "6": 2.0,
        }

        return int(self.ftp_watts * zones[zone])

    # def entries(self):
    #     entries = []
    #     for entry in (
    #         TrainingEntry.objects.select_related("week")
    #         .select_related("season")
    #         .filter(season=self)
    #     ):
    #         # diff = (entry.entry_date - entry.week.week_start_date).days
    #         entries.append(entry)
    #
    #     return entries
    #
    # def workouts(self, start_date=None, end_date=None):
    #     if start_date is None:
    #         start_date = self.season_start_date
    #
    #     if end_date is None:
    #         end_date = self.season_end_date
    #
    #     workouts = defaultdict(list)
    #     for workout in StravaActivity.objects.filter(
    #         start_datetime__range=(start_date, end_date)
    #     ):
    #         workouts[workout.start_datetime_local.date()].append(workout)
    #
    #     return workouts
    #
    # def __unicode__(self):
    #     return "%s" % (self.season_start_date,)
    #
    # def update_basic_weeks(self):
    #     progression = tp_from_season(self).progression()
    #
    #     weeks = []
    #     this_day = self.season_start_date
    #     prog_index = 0
    #     prog_ct = 1
    #     week_prog = progression[prog_index]
    #     while this_day <= self.season_end_date:
    #         if prog_ct > week_prog[1]:
    #             prog_ct = 1
    #             if prog_index < len(progression) - 1:
    #                 prog_index += 1
    #
    #         week_prog = progression[prog_index]
    #
    #         try:
    #             w = TrainingWeek.objects.get(week_start_date=this_day)
    #             w.season = self
    #             w.week_type = week_prog[0]
    #             w.week_type_num = prog_ct
    #         except TrainingWeek.DoesNotExist:
    #             w = TrainingWeek(
    #                 season=self,
    #                 week_start_date=this_day,
    #                 week_type=week_prog[0],
    #                 week_type_num=prog_ct,
    #             )
    #             w.save()  # ??
    #         w.populate_entries()
    #         weeks.append(w)
    #
    #         next_day = this_day + datetime.timedelta(days=7)
    #
    #         this_day = next_day
    #         prog_ct += 1
    #
    #     for week in weeks:
    #         week.save()
    #
    #     return weeks
