# import datetime
# import logging
# import urllib
# from collections import defaultdict
#
# import pytz
# from bikething import stravaapi
# from django.contrib.auth.models import User
# from django.core.urlresolvers import reverse
# from django.db import models
#
# from . import data
#
# logger = logging.getLogger(__name__)
#
# tz = pytz.timezone('US/Central')
# def tznow():
#     return tz.localize(datetime.datetime.now())
#
# # Profile for the season
# class Season(models.Model):
#     LIMIT_FACTOR_CHOICES = (
#         ('Strength', 'Strength'),
#         ('Speed', 'Speed'),
#         ('Muscualar-Endurance', 'Muscualar-Endurance'),
#         ('Speed-Endurance', 'Speed-Endurance'),
#         ('Power', 'Power'),
#     )
#
#     user = models.ForeignKey(User)
#     limiting_factors_1 = models.CharField(max_length=50, choices=LIMIT_FACTOR_CHOICES)
#     limiting_factors_2 = models.CharField(max_length=50, choices=LIMIT_FACTOR_CHOICES)
#     season_start_date = models.DateField()
#     season_end_date = models.DateField()
#     annual_hours = models.IntegerField()
#
#     # ftp_hr = 170  This is what I got from Rubber Glove last year but holy crap
#     ftp_hr = 167
#     ftp_watts = 247
#
#     def zone_hr(self, zone):
#         zones = {
#             "": 0,
#             "1": .81,
#             "2": .89,
#             "3": .93,
#             "4": .99,
#             "5a": 1.02,
#             "5b": 1.06,
#             "5c": 1.10,
#             "6": 1.10,
#         }
#
#         return int(self.ftp_hr*zones[zone])
#
#     def zone_power(self, zone):
#         zones = {
#             "": 0,
#             "1": .55,
#             "2": .74,
#             "3": .89,
#             "4": 1.04,
#             "5a": 1.12,
#             "5b": 1.17,
#             "5c": 1.2,
#             "6": 2.0,
#         }
#
#         return int(self.ftp_watts*zones[zone])
#
#
#     def entries(self):
#         entries = []
#         for entry in Entry.objects.select_related('week').select_related('season').filter(season=self):
#             #diff = (entry.entry_date - entry.week.week_start_date).days
#             entries.append(entry)
#
#         return entries
#
#     def workouts(self, start_date=None, end_date=None):
#         if start_date is None:
#             start_date = self.season_start_date
#
#         if end_date is None:
#             end_date = self.season_end_date
#
#         workouts = defaultdict(list)
#         for workout in StravaActivity.objects.filter(start_datetime__range=(start_date, end_date)):
#             workouts[workout.start_datetime_local.date()].append(workout)
#
#         return workouts
#
#     def __unicode__(self):
#         return "%s" % (self.season_start_date, )
#
# class Week(models.Model):
#     WEEK_TYPE_CHOICES = (
#         ('Prep', 'Prep'),
#         ('Base 1', 'Base 1'),
#         ('Base 2', 'Base 2'),
#         ('Base 3', 'Base 3'),
#         ('Build 1', 'Build 1'),
#         ('Build 2', 'Build 2'),
#         ('Peak', 'Peak'),
#         ('RaceSat', 'Race Saturday'),
#         ('RaceSun', 'Race Sunday'),
#         ('RaceSatSun', 'Race Saturday and Sunday'),
#         ('Transition', 'Transition'),
#     )
#
#     week_start_date = models.DateField()
#     season = models.ForeignKey(Season, unique_for_date="week_start_date")
#     week_type = models.CharField(max_length=50, choices=WEEK_TYPE_CHOICES)
#     week_type_num = models.IntegerField()
#
#     def __unicode__(self):
#         return "%s:%s-%s" % (self.week_start_date, self.week_type, self.week_type_num)
#
#     def json(self, cal):
#         output = {}
#         output['entries'] = []
#         for elist in cal.entries_by_week(self):
#             output['entries'].append([e.json() for e in elist])
#
#         for el in ('week_type', ):
#             output[el] = getattr(self, el)
#
#         output['week_start_date'] = self.week_start_date
#
#         return output
#
#     def races(self, race_filter=None):
#         if race_filter is None:
#             race_filter = Race.objects.filter(season=self.season)
#
#         f = race_filter.select_related('week').filter(race_date__gte=self.week_start_date)
#         f = f.filter(race_date__lt=self.week_start_date + datetime.timedelta(days=7))
#
#         return f
#
#     def weekly_hours(self):
#         yearlies = data.annual_hours_lookup['Yearly']
#         i = yearlies.index(self.season.annual_hours)
#
#         try:
#             key = "%s-%s" % (self.week_type, self.week_type_num)
#             hours = data.annual_hours_lookup[key][i]
#         except KeyError:
#             key = "%s" % (self.week_type, )
#             hours = data.annual_hours_lookup[key][i]
#
#         return hours
#
#     def entries(self, populate=False):
#         if populate:
#             self.populate_entries(delete_first=True)
#
#         m = {}
#         for d in range(7): m[d] = []
#         for entry in Entry.objects.select_related('week').filter(week=self):
#             diff = (entry.entry_date - self.week_start_date).days
#             m[diff].append(entry)
#
#         return m.values()
#
#     def populate_entries(self, delete_first=False):
#         entry_by_orig = {}
#         if delete_first:
#             Entry.objects.filter(week=self).delete()
#         else:
#             saved_entries = Entry.objects.filter(week=self)
#             for entry in saved_entries:
#                 entry_by_orig[entry.scheduled_dow] = entry
#
#         try:
#             key = "%s-%s" % (self.week_type, self.week_type_num)
#             patterns = data.workout_patterns[key]
#         except KeyError:
#             key = "%s" % (self.week_type, )
#             patterns = data.workout_patterns[key]
#
#         try:
#             key = "%s-%s" % (self.week_type, self.week_type_num)
#             hpatterns = data.hour_patterns[key]
#         except KeyError:
#             key = "%s" % (self.week_type, )
#             hpatterns = data.hour_patterns[key]
#
#
#         week_hours = data.weekly_hours_lookup[self.weekly_hours()]
#         start_index = (int(self.week_start_date.strftime("%w"))-1) % 7
#
#         for dow in range(0, 7):
#             dow_ind = (dow + start_index) % 7
#             wotype = patterns[dow_ind][0]
#
#             if dow not in entry_by_orig:
#                 entry = Entry(entry_date=self.week_start_date + datetime.timedelta(days=dow),
#                               season=self.season,
#                               week=self,
#                               workout_type=wotype,
#                               scheduled_dow=dow_ind,
#                               scheduled_length=week_hours[hpatterns[dow_ind]-1],
#                               actual_length=week_hours[hpatterns[dow_ind]-1],
#                               )
#
#                 entry.save()
#
#     def is_this_week(self):
#         today = datetime.date.today()
#         return self.week_start_date <= today and today < self.week_start_date + datetime.timedelta(days=7)
#
#
#
# # This holds the user's particular schedule, to let them select things
# # and move them around
# class Entry(models.Model):
#     NAME_CHOICES = (
#         ('E1', 'Recovery'),
#         ('E2', 'Aerobic'),
#         ('E3', 'Fixed Gear'),
#         ('F1', 'Moderate Hills'),
#         ('F2', 'Long Hills'),
#         ('F3', 'Steep Hills'),
#         ('S1', 'Spin-ups'),
#         ('S2', 'Isolated Leg'),
#         ('S3', 'Cornering'),
#         ('S4', 'Bumping'),
#         ('S5', 'Form Sprints'),
#         ('S6', 'Sprints'),
#         ('M1', 'Tempo'),
#         ('M2', 'Cruise Intervals'),
#         ('M3', 'Hill Cruise Intervals'),
#         ('M4', 'Motorpaced Cruise Intervals'),
#         ('M5', 'Criss-Cross Threshold'),
#         ('M6', 'Threshold'),
#         ('M7', 'Motorpaced Threshold'),
#         ('A1', 'Group Ride'),
#         ('A2', 'SE Intervals'),
#         ('A3', 'Pyramid Intervals'),
#         ('A4', 'Hill Intervals'),
#         ('A5', 'Lactate Tolerance Reps'),
#         ('A6', 'Hill Reps'),
#         ('P1', 'Jumps'),
#         ('P2', 'Hill Sprints'),
#         ('P3', 'Crit Sprints'),
#         ('T1', 'Aerobic Time Trial'),
#         ('T2', 'Time Trial'),
#         ('RACE', 'Race'),
#         ('OFF', 'Off'),
#         )
#
#     entry_date = models.DateField()
#     season = models.ForeignKey(Season, unique_for_date="entry_date")
#     week = models.ForeignKey(Week)
#     workout_type = models.CharField(max_length=50, choices=NAME_CHOICES)
#     scheduled_dow = models.IntegerField()
#     scheduled_length = models.FloatField()
#     actual_length = models.FloatField()
#     notes = models.CharField(max_length=2000)
#
#     def __unicode__(self):
#         return "%s" % (self.entry_date, )
#
#     def json(self):
#         output = {}
#
#         for el in ('id', 'entry_date', 'workout_type', 'scheduled_dow', 'scheduled_length', 'actual_length'):
#             output[el] = getattr(self, el)
#
#         output['workout_types'] = self.workout_type_list()
#
#         return output
#
#     def workout_type_list(self):
#         try:
#             key = "%s-%s" % (self.week.week_type, self.week.week_type_num)
#             patterns = data.workout_patterns[key]
#         except KeyError:
#             key = "%s" % (self.week.week_type, )
#             patterns = data.workout_patterns[key]
#
#         #hours = data.weekly_hours_lookup[self.week.weekly_hours()][self.scheduled_dow]
#         return patterns[self.scheduled_dow]
#
#     def link(self, workout_type):
#         if self.workout_type == workout_type:
#             return "<b>%s</b>" % workout_type
#         else:
#             wt = workout_type
#
#             url = "<a href='%s?%s'>%s</a>" % (
#                 reverse('update_entry', kwargs={'entry_id': self.id}),
#                 urllib.urlencode({'workout_type': workout_type}),
#                 wt,
#             )
#             return url
#
#     def is_today(self):
#         return datetime.date.today() == self.entry_date
#
#     def workout_description(self, wo_type):
#         return data.workouts[wo_type]
#
# class Race(models.Model):
#     PRIORITY_CHOICES = (('A', 'A'), ('B', 'B'), ('C', 'C'))
#
#     season = models.ForeignKey(Season)
#     race_date = models.DateField()
#     name = models.CharField(max_length=100)
#     location = models.CharField(max_length=100)
#     priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES)
#
#     def __unicode__(self):
#         return "%s -- %s" % (self.name, self.race_date)
#
#
# class Calendar(object):
#     def __init__(self, user=None, all=False):
#         self.user = user
#
#         self.season = list(Season.objects.filter(user=self.user).order_by('season_start_date'))[-1]
#         self.races = Race.objects.filter(season=self.season)
#
#         self.start_date = self.season.season_start_date
#         self.end_date = self.season.season_end_date
#
#         self.all = all
#
#         if all:
#             self.entries = self.season.entries()
#             self.workouts = self.season.workouts()
#         else:
#             self.select_start = tznow() - datetime.timedelta(weeks=2)
#             self.select_end = tznow() + datetime.timedelta(weeks=1)
#             self.entries = Entry.objects.select_related('week').select_related('season').filter(week__week_start_date__range=(self.select_start, self.select_end))
#
#             self.workouts = self.season.workouts(start_date=self.select_start, end_date=self.select_end)
#
#     def update_basic_weeks(self):
#         progression = (
#             ('Prep', 4),
#             ('Base 1', 4),
#             ('Base 2', 4),
#             ('Base 3', 4),
#             ('Build 1', 4),
#             ('Build 2', 4),
#             ('Peak', 2),
#             ('RaceSat', 1),
#             ('Build 1', 3),
#             ('Peak', 2),
#             ('RaceSat', 1),
#             ('Peak', 2),
#             ('RaceSat', 1),
#             ('Transition', 1),
#             ('Base 3', 4),
#             ('Build 1', 4),
#             ('Build 2', 4),
#             ('Peak', 2),
#             ('RaceSat', 2),
#             ('Transition', 1)
#         )
#
#         weeks = []
#         this_day = self.start_date
#         week_type = 'Prep'
#         prog_index = 0
#         prog_ct = 1
#         week_prog = progression[prog_index]
#         while this_day <= self.end_date:
#             if prog_ct > week_prog[1]:
#                 prog_ct = 1
#                 if prog_index < len(progression)-1:
#                     prog_index += 1
#
#             week_prog = progression[prog_index]
#
#             try:
#                 w = Week.objects.get(week_start_date=this_day)
#                 w.week_type = week_prog[0]
#                 w.week_type_num = prog_ct
#             except Week.DoesNotExist:
#                 w = Week(season=self.season,
#                          week_start_date=this_day,
#                          week_type=week_prog[0],
#                          week_type_num=prog_ct
#                 )
#                 w.save()  # ??
#             w.populate_entries()
#             weeks.append(w)
#
#             next_day = this_day + datetime.timedelta(days=7)
#
#             this_day = next_day
#             prog_ct += 1
#
#         for week in weeks:
#             week.save()
#
#         return weeks
#
#     def weeks(self, week_start_date=None):
#         if week_start_date:
#             return Week.objects.select_related('season').filter(week_start_date=week_start_date).order_by('week_start_date')
#         elif self.all:
#             return Week.objects.select_related('season').filter(season=self.season).order_by('week_start_date')
#         else:
#             return Week.objects.select_related('season').filter(week_start_date__range=(self.select_start, self.select_end)).order_by('week_start_date')
#
#     def entries_by_week(self, week):
#         m = {}
#         for d in range(7):
#             m[d] = []
#         for entry in [x for x in self.entries if x.week.id == week.id]:
#             diff = (entry.entry_date - week.week_start_date).days
#
#             try:
#                 m[diff].append(entry)
#             except KeyError, e:
#                 pass
#
#         return m.values()
#
#     def workouts_from_date(self, date):
#         return self.workouts[date]
#
#     def strava_workout_hours(self, week_start_date):
#         hours = 0
#         for day in range(7):
#             woday = week_start_date + datetime.timedelta(days=day)
#             hours += sum([wo.moving_time/(60.0*60) for wo in self.workouts_from_date(woday)])
#
#         return hours
#
#     def strava_workouts(self, week_start_date):
#         wo = sum([self.workouts_from_date(week_start_date + datetime.timedelta(days=day)) for day in range(7)], [])
#         logger.warn('wo=%r', wo)
#         return wo
#
#
#
# class StravaActivity(models.Model):
#
#     def json(self):
#         return {
#             'user_id': self.user.id,
#             'start_datetime_local': self.start_datetime_local,
#             'activity_id': self.activity_id,
#             'activity_name': self.activity_name,
#             'distance_miles': self.distance_miles(),
#             'moving_time': self.moving_time,
#             'total_elevation_gain_feet': self.total_elevation_gain_feet(),
#             'average_watts': self.average_watts,
#             'average_heartrate': self.average_heartrate,
#             'suffer_score': self.suffer_score,
#         }
#
#     def average_speed_miles(self):
#         return (self.distance_miles() / (self.moving_time/3600.))
#
#     def distance_miles(self):
#         return self.distance / 1609.34
#
#     def total_elevation_gain_feet(self):
#         return self.total_elevation_gain * 3.28084
#
#     def time_formatted(self, sec):
#         hours = sec / 3600
#         minutes = (sec % 3600) / 60
#         seconds = sec % 60
#         return "%2d:%02d:%02d" % (hours, minutes, seconds)
#
#     def moving_time_formatted(self):
#         return self.time_formatted(self.moving_time)
#
#     def elapsed_time_formatted(self):
#         return self.time_formatted(self.elapsed_time)
#
#     @classmethod
#     def sync_one_byobj(cls, user, activity):
#         data = stravaapi.activity(user, activity.activity_id)
#         cls.sync_one(user, data, full=True, rebuild=True)
#
#
#     @classmethod
#     def update_incomplete(cls, user):
#         incomplete = cls.objects.filter(embed_token__isnull=True)
#
#         updated = 0
#         for activity in incomplete:
#             updated += 1
#             cls.sync_one(user, stravaapi.activity(user, activity.activity_id))
#
#         incomplete = cls.objects.filter(embed_token__isnull=True)
#
#         return updated, len(incomplete)
#
#     @classmethod
#     def update_streams(cls, user):
#         all = cls.objects.filter()
#
#         updated = 0
#         for activity in all:
#             streams = StravaActivityStream.objects.filter(activity=activity)
#             if len(streams):
#                 continue
#
#             logger.warn("Updating stream for %d\n", activity.activity_id)
#             try:
#                 cls.sync_one(user, stravaapi.activity(user, activity.activity_id))
#             except stravaapi.StravaError, e:
#                 logger.error("Error updating stream for %r: %r", activity.activity_id, e)
#                 continue
#
#             updated += 1
#
#             if updated >= 100:
#                 break
#
#         return updated
#
#     @classmethod
#     def update_curves(cls):
#         all = cls.objects.filter()
#
#         updated = 0
#         for activity in all:
#             streams1 = StravaPowerCurve.objects.filter(activity=activity)
#             streams2 = StravaSpeedCurve.objects.filter(activity=activity)
#             if len(streams1) and len(streams2):
#                 continue
#
#             if not len(streams1):
#                 StravaPowerCurve.process_curve(activity.activity_id)
#
#             if not len(streams2):
#                 StravaSpeedCurve.process_curve(activity.activity_id)
#
# 	    updated += 1
#
# #            if updated >= 10:
# #                break
#
#         return updated
#
#
#     def __unicode__(self):
#         return "Strava Activity: %s (%0.1f hours)" % (self.start_datetime_local, self.moving_time/(60.0*60))
#
#
#
#
# class StravaActivityStream(models.Model):
#     def json(self):
#         fields = ['time', 'lat', 'long', 'distance_mi', 'altitude', 'speed_mph', 'heartrate', 'cadence', 'watts', 'temp', 'moving', 'grade_smooth']
#         return {f: getattr(self, f) for f in fields}
#
#
#     @property
#     def distance_mi(self):
#         return self.distance / 1609.34
#
#     @property
#     def speed_mph(self):
#         return (self.velocity_smooth / 1609.34)*3600
#
#
#
