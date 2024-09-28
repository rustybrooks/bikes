from collections import defaultdict
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import json
import logging
import numpy
import pytz
import time
import urllib

# from . import data
from bikething import stravaapi

logger = logging.getLogger(__name__)

tz = pytz.timezone('US/Central')
def tznow():
    return tz.localize(datetime.datetime.now())


from . import plans

tpmap = {
    'CTB': plans.CTB,
    'TCC': plans.TCC,
}

def tp_from_season(s):
    logger.error("tp_from_season - season = %r, params = %r, tp = %r", s, s.params, s.training_plan)
    return tpmap[s.training_plan](json.loads(s.params))

# Profile for the season
class Season(models.Model):
    # LIMIT_FACTOR_CHOICES = (
    #     ('Strength', 'Strength'),
    #     ('Speed', 'Speed'),
    #     ('Muscualar-Endurance', 'Muscualar-Endurance'),
    #     ('Speed-Endurance', 'Speed-Endurance'),
    #     ('Power', 'Power'),
    # )

    TP_CHOICES = (
        ('CTB', 'Cyclist\'s Training Bible'),
        ('TCC', 'Time Crunched Cyclist'),
    )

    user = models.ForeignKey(User)
    # limiting_factors_1 = models.CharField(max_length=50, choices=LIMIT_FACTOR_CHOICES)
    # limiting_factors_2 = models.CharField(max_length=50, choices=LIMIT_FACTOR_CHOICES)
    training_plan = models.CharField(max_length=100, choices=TP_CHOICES)
    season_start_date = models.DateField()
    season_end_date = models.DateField()
    # annual_hours = models.IntegerField()
    params = models.CharField(max_length=5000)

    # ftp_hr = 170  This is what I got from Rubber Glove last year but holy crap
    ftp_hr = 167
    ftp_watts = 247

    def zone_hr(self, zone):
        zones = {
            "": 0,
            "1": .81,
            "2": .89,
            "3": .93,
            "4": .99,
            "5a": 1.02,
            "5b": 1.06,
            "5c": 1.10,
            "6": 1.10,
        }

        return int(self.ftp_hr*zones[zone])

    def zone_power(self, zone):
        zones = {
            "": 0,
            "1": .55,
            "2": .74,
            "3": .89,
            "4": 1.04,
            "5a": 1.12,
            "5b": 1.17,
            "5c": 1.2,
            "6": 2.0,
        }

        return int(self.ftp_watts*zones[zone])


    def entries(self):
        entries = []
        for entry in Entry.objects.select_related('week').select_related('season').filter(season=self):
            #diff = (entry.entry_date - entry.week.week_start_date).days
            entries.append(entry)

        return entries

    def workouts(self, start_date=None, end_date=None):
        if start_date is None:
            start_date = self.season_start_date

        if end_date is None:
            end_date = self.season_end_date

        workouts = defaultdict(list)
        for workout in StravaActivity.objects.filter(start_datetime__range=(start_date, end_date)):
            workouts[workout.start_datetime_local.date()].append(workout)

        return workouts

    def __unicode__(self):
        return "%s" % (self.season_start_date, )

    def update_basic_weeks(self):

        print tp_from_season(self)

        progression = tp_from_season(self).progression()

        weeks = []
        this_day = self.season_start_date
        week_type = progression[0]
        prog_index = 0
        prog_ct = 1
        week_prog = progression[prog_index]
        while this_day <= self.season_end_date:
            if prog_ct > week_prog[1]:
                prog_ct = 1
                if prog_index < len(progression)-1:
                    prog_index += 1

            week_prog = progression[prog_index]

            try:
                w = Week.objects.get(week_start_date=this_day)
                w.season = self
                w.week_type = week_prog[0]
                w.week_type_num = prog_ct
            except Week.DoesNotExist:
                w = Week(season=self,
                         week_start_date=this_day,
                         week_type=week_prog[0],
                         week_type_num=prog_ct
                )
                w.save()  # ??
            w.populate_entries()
            weeks.append(w)

            next_day = this_day + datetime.timedelta(days=7)

            this_day = next_day
            prog_ct += 1

        for week in weeks:
            week.save()

        return weeks

class Week(models.Model):
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
    season = models.ForeignKey(Season, unique_for_date="week_start_date")
    week_type = models.CharField(max_length=50)  # , choices=WEEK_TYPE_CHOICES
    week_type_num = models.IntegerField()

    def __unicode__(self):
        return "%s:%s-%s" % (self.week_start_date, self.week_type, self.week_type_num)

    def json(self, cal):
        output = {}
        output['entries'] = []
        for elist in cal.entries_by_week(self):
            output['entries'].append([e.json() for e in elist])

        for el in ('week_type', ):
            output[el] = getattr(self, el)

        output['week_start_date'] = self.week_start_date

        return output

    def races(self, race_filter=None):
        if race_filter is None:
            race_filter = Race.objects.filter(season=self.season)

        f = race_filter.select_related('week').filter(race_date__gte=self.week_start_date)
        f = f.filter(race_date__lt=self.week_start_date + datetime.timedelta(days=7))

        return f

    def weekly_hours(self):
        logger.warn("tp_from_season... %r", self.week_start_date)
        tp = tp_from_season(self.season)
        return tp.weekly_hours(self)

    def entries(self, populate=False):
        if populate:
            self.populate_entries(delete_first=True)

        m = {}
        for d in range(7): m[d] = []
        for entry in Entry.objects.select_related('week').filter(week=self):
            diff = (entry.entry_date - self.week_start_date).days
            m[diff].append(entry)

        return m.values()

    def populate_entries(self, delete_first=False):
        entry_by_orig = {}
        if delete_first:
            Entry.objects.filter(week=self).delete()
        else:
            saved_entries = Entry.objects.filter(week=self)
            for entry in saved_entries:
                entry_by_orig[entry.scheduled_dow] = entry

        tp = tp_from_season(self.season)
        for e in tp.plan_entries(self):
            dow = e.pop('dow')
            if dow in entry_by_orig:
                continue
            e['season'] = self.season
            e['week'] = self
            e['entry_date'] = self.week_start_date + datetime.timedelta(days=dow)
            entry = Entry(**e)
            entry.save()

    def is_this_week(self):
        today = datetime.date.today()
        return self.week_start_date <= today and today < self.week_start_date + datetime.timedelta(days=7)



# This holds the user's particular schedule, to let them select things 
# and move them around
class Entry(models.Model):
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
    season = models.ForeignKey(Season, unique_for_date="entry_date")
    week = models.ForeignKey(Week)
    workout_type = models.CharField(max_length=50)  # , choices=NAME_CHOICES
    scheduled_dow = models.IntegerField()
    scheduled_length = models.FloatField()
    scheduled_length2 = models.FloatField()
    actual_length = models.FloatField()
    notes = models.CharField(max_length=2000)

    def __unicode__(self):
        return "%s" % (self.entry_date, )

    def json(self):
        output = {}

        for el in ('id', 'entry_date', 'workout_type', 'scheduled_dow', 'scheduled_length', 'actual_length'):
            output[el] = getattr(self, el)

        output['workout_types'] = self.workout_type_list()

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
                reverse('update_entry', kwargs={'entry_id': self.id}),
                urllib.urlencode({'workout_type': workout_type}),
                wt,
            )
            return url

    def is_today(self):
        return datetime.date.today() == self.entry_date

    def workout_description(self, wo_type):
        tp = tp_from_season(self.season)
        return tp.workout_description(wo_type)

class Race(models.Model):
    PRIORITY_CHOICES = (('A', 'A'), ('B', 'B'), ('C', 'C'))

    season = models.ForeignKey(Season)
    race_date = models.DateField()
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES)

    def __unicode__(self):
        return "%s -- %s" % (self.name, self.race_date)


class Calendar(object):
    def __init__(self, user=None, all=False):
        self.user = user

        self.season = list(Season.objects.filter(user=self.user).order_by('season_start_date'))[-1]
        self.races = Race.objects.filter(season=self.season)

        self.start_date = self.season.season_start_date
        self.end_date = self.season.season_end_date

        self.all = all

        if all:
            self.entries = self.season.entries()
            self.workouts = self.season.workouts()
        else:
            self.select_start = tznow() - datetime.timedelta(weeks=2)
            self.select_end = tznow() + datetime.timedelta(weeks=1)
            self.entries = Entry.objects.select_related('week').select_related('season').filter(week__week_start_date__range=(self.select_start, self.select_end))

            self.workouts = self.season.workouts(start_date=self.select_start, end_date=self.select_end)

    def weeks(self, week_start_date=None):
        if week_start_date:
            return Week.objects.select_related('season').filter(week_start_date=week_start_date).order_by('week_start_date')
        elif self.all:
            return Week.objects.select_related('season').filter(season=self.season).order_by('week_start_date')
        else:
            return Week.objects.select_related('season').filter(week_start_date__range=(self.select_start, self.select_end)).order_by('week_start_date')

    def entries_by_week(self, week):
        m = {}
        for d in range(7):
            m[d] = []
        for entry in [x for x in self.entries if x.week.id == week.id]:
            diff = (entry.entry_date - week.week_start_date).days

            try:
                m[diff].append(entry)
            except KeyError, e:
                pass

        return m.values()

    def workouts_from_date(self, date):
        return self.workouts[date]

    def strava_workout_hours(self, week_start_date):
        hours = 0
        for day in range(7):
            woday = week_start_date + datetime.timedelta(days=day)
            hours += sum([wo.moving_time/(60.0*60) for wo in self.workouts_from_date(woday)])

        return hours

    def strava_workouts(self, week_start_date):
        wo = sum([self.workouts_from_date(week_start_date + datetime.timedelta(days=day)) for day in range(7)], [])
        logger.warn('wo=%r', wo)
        return wo



class StravaActivity(models.Model):
    user = models.ForeignKey(User)
    activity_id = models.BigIntegerField(primary_key=True)
    external_id = models.TextField(null=True)
    upload_id = models.BigIntegerField(null=True)
    athlete_id = models.BigIntegerField()
    activity_name = models.TextField(null=True)
    distance = models.FloatField()
    moving_time = models.IntegerField()
    elapsed_time = models.IntegerField()
    total_elevation_gain = models.FloatField()
    elev_high = models.FloatField(null=True)
    elev_low = models.FloatField(null=True)
    type = models.TextField()
    start_datetime = models.DateTimeField(null=True)
    start_datetime_local = models.DateTimeField()
    timezone = models.TextField()
    start_lat = models.FloatField(null=True)
    start_long = models.FloatField(null=True)
    end_lat = models.FloatField(null=True)
    end_long = models.FloatField(null=True)
    achievement_count = models.IntegerField()
    athlete_count = models.IntegerField()
    # map # I dunno
    trainer = models.BooleanField(default=False)
    commute = models.BooleanField(default=False)
    manual = models.BooleanField(default=False)
    private = models.BooleanField(default=False)
    embed_token = models.TextField(null=True)
    flagged = models.BooleanField(default=False)
    workout_type = models.IntegerField(null=True)
    gear_id = models.TextField(null=True)
    average_speed = models.FloatField(null=True)
    max_speed = models.FloatField(null=True)
    average_cadence = models.FloatField(null=True)
    average_temp = models.FloatField(null=True)
    average_watts = models.FloatField(null=True)
    max_watts = models.FloatField(null=True)
    weighted_average_watts = models.FloatField(null=True)
    kilojoules = models.FloatField(null=True)
    device_watts = models.NullBooleanField(default=False)
    average_heartrate = models.FloatField(null=True)
    max_heartrate = models.FloatField(null=True)
    suffer_score = models.IntegerField(null=True)

    def json(self):
        return {
            'user_id': self.user.id,
            'start_datetime_local': self.start_datetime_local,
            'activity_id': self.activity_id,
            'activity_name': self.activity_name,
            'distance_miles': self.distance_miles(),
            'moving_time': self.moving_time,
            'total_elevation_gain_feet': self.total_elevation_gain_feet(),
            'average_watts': self.average_watts,
            'average_heartrate': self.average_heartrate,
            'suffer_score': self.suffer_score,
        }

    def average_speed_miles(self):
        return (self.distance_miles() / (self.moving_time/3600.))

    def distance_miles(self):
        return self.distance / 1609.34

    def total_elevation_gain_feet(self):
        return self.total_elevation_gain * 3.28084

    def time_formatted(self, sec):
        hours = sec / 3600
        minutes = (sec % 3600) / 60
        seconds = sec % 60
        return "%2d:%02d:%02d" % (hours, minutes, seconds)

    def moving_time_formatted(self):
        return self.time_formatted(self.moving_time)

    def elapsed_time_formatted(self):
        return self.time_formatted(self.elapsed_time)

    @classmethod
    def sync_one_byobj(cls, user, activity):
        data = stravaapi.activity(user, activity.activity_id)
        cls.sync_one(user, data, full=True, rebuild=True)

    @classmethod
    def sync_one(cls, user, activity, full=False, rebuild=False):
        activity_id = activity['id']
        actlist = cls.objects.filter(activity_id=activity_id)

        # If we already have this one, let's not resync
        if len(actlist) and not rebuild:
            return

        if 'segment_efforts' not in activity and full:
            return cls.sync_one(user, stravaapi.activity(user, activity['id']))

        new = False
        if len(actlist):
            act = actlist[0]
        else:
            act = StravaActivity()
            act.activity_id = activity_id
            act.user = user
            new = True

        for key in [
            'external_id', 'upload_id', 'activity_name', 'distance', 'moving_time',
            'elapsed_time', 'total_elevation_gain', 'elev_high', 'elev_low', 'type', 'timezone',
            'achievement_count', 'athlete_count', 'trainer', 'commute', 'manual', 'private', 'embed_token',
            'workout_type', 'gear_id', 'average_speed', 'max_speed', 'average_cadence', 'average_temp', 'average_watts',
            'max_watts', 'weighted_average_watts', 'kilojoules', 'device_watts', 'average_heartrate', 'max_heartrate',
            'suffer_score', 'flagged'
        ]:
            setattr(act, key, activity.get(key))

        act.athlete_id = activity['athlete']['id']

        act.start_datetime = activity['start_date']
        act.start_datetime_local = activity['start_date_local']

        act.start_lat = activity['start_latlng'][0] if activity['start_latlng'] else None
        act.start_long = activity['start_latlng'][1] if activity['start_latlng'] else None
        act.end_lat = activity['end_latlng'][0] if activity['end_latlng'] else None
        act.end_long = activity['end_latlng'][1] if activity['end_latlng'] else None

        act.save()

        if 'segment_efforts' in activity:
            for e in activity.get('segment_efforts', []):
                effort = StravaActivitySegmentEffort.sync_one(act, e)

                if new:
                    StravaSegmentHistory.sync_one(user, effort.segment_id, act.athlete_id)

        StravaActivityStream.sync(user, act)

        return act

    @classmethod
    def sync_many(cls, user):
        first_date = tznow() - datetime.timedelta(days=14)

        activities = stravaapi.activities(user, after=first_date)
        for act in activities:
            cls.sync_one(user, act, full=True)

    @classmethod
    def update_incomplete(cls, user):
        incomplete = cls.objects.filter(embed_token__isnull=True)

        updated = 0
        for activity in incomplete:
            updated += 1
            cls.sync_one(user, stravaapi.activity(user, activity.activity_id))

        incomplete = cls.objects.filter(embed_token__isnull=True)

        return updated, len(incomplete)

    @classmethod
    def update_streams(cls, user):
        all = cls.objects.filter()

        updated = 0
        for activity in all:
            streams = StravaActivityStream.objects.filter(activity=activity)
            if len(streams):
                continue

            logger.warn("Updating stream for %d\n", activity.activity_id)
            try:
                cls.sync_one(user, stravaapi.activity(user, activity.activity_id))
            except stravaapi.StravaError, e:
                logger.error("Error updating stream for %r: %r", activity.activity_id, e)
                continue

            updated += 1

            if updated >= 100:
                break

        return updated

    @classmethod
    def update_curves(cls):
        all = cls.objects.filter()

        updated = 0
        for activity in all:
            streams1 = StravaPowerCurve.objects.filter(activity=activity)
            streams2 = StravaSpeedCurve.objects.filter(activity=activity)
            if len(streams1) and len(streams2):
                continue

            if not len(streams1):
                StravaPowerCurve.process_curve(activity.activity_id)

            if not len(streams2):
                StravaSpeedCurve.process_curve(activity.activity_id)

	    updated += 1

#            if updated >= 10:
#                break

        return updated


    def __unicode__(self):
        return "Strava Activity: %s (%0.1f hours)" % (self.start_datetime_local, self.moving_time/(60.0*60))


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
        id = segment['id']
        segs = cls.objects.filter(segment_id=id)
        if len(segs):
            seg = segs[0]
        else:
            seg = StravaSegment()
            seg.segment_id = id

        for key in [
            'resource_state', 'name', 'activity_type', 'distance', 'average_grade', 'maximum_grade', 'elevation_high',
            'elevation_low', 'climb_category', 'city', 'state',
            'country', 'private', 'starred', 'created_at', 'updated_at', 'total_elevation_gain', 'effort_count',
            'athlete_count', 'hazardous', 'star_count',
        ]:
            #logger.warn("key = %r, val = %r", key, segment.get(key))
            setattr(seg, key, segment.get(key))

        seg.start_lat = segment['start_latlng'][0] if segment['start_latlng'] else None
        seg.start_long = segment['start_latlng'][1] if segment['start_latlng'] else None
        seg.end_lat = segment['end_latlng'][0] if segment['end_latlng'] else None
        seg.end_long = segment['end_latlng'][1] if segment['end_latlng'] else None

        seg.save()

        return seg


class StravaActivitySegmentEffort(models.Model):
    activity_segment_id = models.BigIntegerField(primary_key=True)
    activity = models.ForeignKey(StravaActivity)
    resource_state = models.IntegerField()
    name = models.TextField()
    elapsed_time = models.IntegerField()
    moving_time = models.IntegerField()
    start_datetime = models.DateTimeField()
    start_datetime_local = models.DateTimeField()
    distance = models.FloatField()
    start_index = models.BigIntegerField()
    end_index = models.BigIntegerField()
    average_cadence = models.FloatField(null=True)
    average_watts = models.FloatField(null=True)
    device_watts = models.NullBooleanField(default=False)
    average_heartrate = models.FloatField(null=True)
    max_heartrate = models.FloatField(null=True)
    segment = models.ForeignKey(StravaSegment)
    kom_rank = models.IntegerField(null=True)
    pr_rank = models.IntegerField(null=True)
    hidden = models.BooleanField(default=False)

    @classmethod
    def sync_one(cls, activity, segment):
        id = segment['id']
        segs = cls.objects.filter(activity_segment_id=id)
        if len(segs):
            sege = segs[0]
        else:
            sege = StravaActivitySegmentEffort()
            sege.activity_segment_id = id

        sege.activity = activity
        sege.start_datetime = segment.get('start_date')
        sege.start_datetime_local = segment.get('start_date_local')

        for key in [
            'resource_state', 'name', 'elapsed_time', 'moving_time', 'distance', 'start_index', 'end_index',
            'average_cadence', 'average_watts', 'device_watts', 'average_heartrate', 'max_heartrate',
            'kom_rank', 'pr_rank', 'hidden'
        ]:
            #logger.warn("key = %r, val = %r", key, segment.get(key))
            setattr(sege, key, segment.get(key))

        sege.segment = StravaSegment.sync_one(segment['segment'])

        sege.save()

        StravaActivitySegmentEffortAch.sync(sege, segment['achievements'])

        return sege


class StravaActivitySegmentEffortAch(models.Model):
    achievement_id = models.AutoField(primary_key=True)
    segment_effort = models.ForeignKey(StravaActivitySegmentEffort)
    type_id = models.IntegerField()
    type = models.TextField()
    rank = models.IntegerField()

    @classmethod
    def sync(cls, segment_effort, achievements):
        #logger.warn("ach = %r", achievements)
        if not len(achievements):
            return

        cls.objects.filter(segment_effort=segment_effort).delete()
        for ach in achievements:
            a = StravaActivitySegmentEffortAch()
            a.segment_effort = segment_effort
            a.type_id = ach['type_id']
            a.type = ach['type']
            a.rank = ach['rank']

            a.save()

class StravaActivityStream(models.Model):
    activity_stream_id = models.AutoField(primary_key=True)
    activity = models.ForeignKey(StravaActivity)
    time = models.IntegerField()
    lat = models.FloatField(null=True)
    long = models.FloatField(null=True)
    distance = models.FloatField(null=True)
    altitude = models.FloatField(null=True)
    velocity_smooth = models.FloatField(null=True)
    heartrate = models.IntegerField(null=True)
    cadence = models.IntegerField(null=True)
    watts = models.IntegerField(null=True)
    temp = models.IntegerField(null=True)
    moving = models.NullBooleanField(default=False)
    grade_smooth = models.FloatField(null=True)

    def json(self):
        fields = ['time', 'lat', 'long', 'distance_mi', 'altitude', 'speed_mph', 'heartrate', 'cadence', 'watts', 'temp', 'moving', 'grade_smooth']
        return {f: getattr(self, f) for f in fields}


    @property
    def distance_mi(self):
        return self.distance / 1609.34
    
    @property
    def speed_mph(self):
        return (self.velocity_smooth / 1609.34)*3600

    # Note, this actually downloads the data too, via the API
    @classmethod
    def sync(cls, user, activity, force=False):
        current = cls.objects.filter(activity=activity)
        if len(current) and not force:
            return

        cls.objects.filter(activity=activity).delete()

        stream_data = stravaapi.activity_stream(user, activity.activity_id)
        types = []
        datas = []
        for stream in stream_data:
            types.append(stream['type'])
            datas.append(stream['data'])

        for datum in zip(*datas):
            #logger.warn("%r", zip(types, datum))
            s = StravaActivityStream()
            s.activity = activity
            for t, d in zip(types, datum):
                if t == 'latlng':
                    s.lat = d[0]
                    s.long = d[1]
                else:
                    setattr(s, t, d)

            s.save()

        StravaPowerCurve.process_curve(activity.activity_id)
        StravaSpeedCurve.process_curve(activity.activity_id)


class StravaSegmentHistorySummary(models.Model):
    segment_history_summary_id = models.AutoField(primary_key=True)
    segment = models.ForeignKey(StravaSegment)
    activity = models.ForeignKey(StravaActivity)

class StravaSegmentHistory(models.Model):
    segment_history_id = models.AutoField(primary_key=True)
    segment = models.ForeignKey(StravaSegment)
    activity = models.ForeignKey(StravaActivity)
    recorded_datetime = models.DateTimeField()
    rank = models.IntegerField()
    entries = models.IntegerField()
    average_hr = models.FloatField(null=True)
    average_watts = models.FloatField(null=True)
    distance = models.FloatField(null=True)
    elapsed_time = models.IntegerField()
    moving_time = models.IntegerField()

    @classmethod
    def sync_one(cls, user, segment_id, athlete_id):
        try:
            leaderboard = stravaapi.segment_leaderboard(user, segment_id)
        except stravaapi.StravaError:
            logger.warn("Failed to fetch segment leaderboard for segment id %d", segment_id)
            return

        # get current best and don't write if it's not better?


        logger.info("Syncing %r", segment_id)
        for el in leaderboard['entries']:
            if el['athlete_id'] == athlete_id:
                # is this the same information we already had?
                existing = StravaSegmentHistorySummary.objects.filter(segment_id=segment_id)
                if len(existing) and existing[0].activity.activity_id == el['activity_id']:
                    break

                x = StravaSegmentHistory()
                x.segment_id = segment_id
                x.entries = leaderboard['entry_count']
                x.activity_id = el['activity_id']
                x.recorded_datetime = tznow()
                for key in ['rank', 'average_hr', 'average_watts', 'distance', 'elapsed_time', 'moving_time']:
                    setattr(x, key, el[key])

                x.save()

                y = StravaSegmentHistorySummary()
                y.segment_id = segment_id
                y.activity_id = el['activity_id']
                y.save()

                break


    @classmethod
    def sync_all(cls, user, athlete_id):
        import time
        segments = StravaSegment.objects.filter()
        for s in segments:
            try:
                cls.sync_one(user, s.segment_id, athlete_id)
                time.sleep(2)
            except stravaapi.StravaError:
                logger.error("Error while syncing segment %r", s.segment_id)


class StravaPowerCurve(models.Model):
    power_curve_id = models.AutoField(primary_key=True)
    interval_length = models.IntegerField()
    watts = models.FloatField()
    activity = models.ForeignKey(StravaActivity)

    @classmethod
    def window(cls, data, length):
        w = numpy.ones(length,'d')
        x = numpy.array([a[1] for a in data])

        if len(w) > len(x):
            return 0

        s = x
        y = numpy.convolve(w/w.sum(),s,mode='same')
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
        this_segment = []

        last = None
        first = None
        stream_data = StravaActivityStream.objects.filter(activity_id=activity_id).order_by('time')
        if not len(stream_data):
            logger.warn("No stream data for %d", activity_id)
            return 

        logger.warn("Processing power curve for %d\n", activity_id)

        for dat in stream_data:
            row = (dat.time, dat.watts if dat.watts else 0)

            if last:
                diff = row[0] - last[0]

                if abs(diff) > 15:
                    segments.append(this_segment)
                    this_segment = []
                elif abs(diff) > 1:
                    for i in range(1, int(diff)):
                        this_segment.append((last[0]+i, last[1]))

                this_segment.append(row)
            else:
                first = row[0]

            last = row

        segments.append(this_segment)

        max_seconds = row[0] - first
        intervals = range(1, 10, 1)
        intervals.extend(range(10, 5*60, 10))
        intervals.extend(range(5*60, 15*60, 30))
        intervals.extend(range(15*60, max_seconds, 60))

        for win in intervals:
            val = max([cls.window(s, win) for s in segments])
            if val == 0:
                continue

            p = StravaPowerCurve()
            p.interval_length = win
            p.watts = val
            p.activity_id = activity_id
            p.start_index = 0
            p.end_index = 0
            p.save()


class StravaSpeedCurve(models.Model):
    speed_curve_id = models.AutoField(primary_key=True)
    interval_length = models.IntegerField()
    speed = models.FloatField()
    activity = models.ForeignKey(StravaActivity)

    @property
    def speed_mph(self):
        return (self.speed / 1609.34)*3600

    @classmethod
    def window(cls, data, length):
        if length >= len(data):
            return 0

        x = numpy.array([a[2] for a in data])
        tm = numpy.array([a[0] for a in data])
        distw = x[length:] - x[:-length]
        tmw = tm[length:] - tm[:-length]
        speed = distw/tmw
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
        this_segment = []

        stream_data = StravaActivityStream.objects.filter(activity_id=activity_id).order_by('time')
        if not len(stream_data):
            logger.warn("No stream data for %d", activity_id)
            return 

        logger.warn("Processing power curve for %d\n", activity_id)

        last = None
        first = None
        for dat in stream_data:
            row = dat.time, dat.velocity_smooth if dat.velocity_smooth else 0, dat.distance if dat.distance else 0

            if last:
                diff = row[0] - last[0]

                if abs(diff) > 15:
                    segments.append(this_segment)
                    this_segment = []
                elif abs(diff) > 1:
                    for i in range(1, int(diff)):
                        this_segment.append((last[0]+i, last[1], last[2]))

                this_segment.append(row)
            else:
                first = row[0]

            last = row

        segments.append(this_segment)

        max_seconds = row[0] - first
        intervals = range(1, 10, 1)
        intervals.extend(range(10, 5*60, 10))
        intervals.extend(range(5*60, 15*60, 30))
        intervals.extend(range(15*60, max_seconds, 60))

        for win in intervals:
            val = max([cls.window(s, win) for s in segments])

            if val == 0:
                continue

#            logger.warn("Adding point %r", (activity_id_, interval_length, val)
            s = StravaSpeedCurve()
            s.interval_length = win
            s.speed = val
            s.activity_id = activity_id
            s.start_index = 0
            s.end_index = 0
            s.save()


