import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, redirect
import dateutil.parser
import logging
import pytz
import json

import bikecal.models as models

logger = logging.getLogger(__name__)

class JSONResponse(HttpResponse):
    def __init__(self, data=None, status=200):
        super(JSONResponse, self).__init__(content=json.dumps(data or {}, default=json_serial), status=status, content_type='application/json')

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime.datetime, datetime.date)):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")

@login_required
def week(request, week_start_date):
    cal = models.Calendar(user=request.user, all=request.REQUEST.get('all', False))
    week = cal.weeks(dateutil.parser.parse(week_start_date))[0]

    return JSONResponse(week.json(cal))


@login_required
def week_by_offset(request, week_offset):
    cal = models.Calendar(user=request.user, all=request.REQUEST.get('all', False))
    season_start = cal.season.season_start_date
    today = pytz.timezone('US/Central').localize(datetime.datetime.now())
    this_week_start = today - datetime.timedelta(days=(today.weekday() - season_start.weekday())%7)
    week = cal.weeks(this_week_start + datetime.timedelta(weeks=int(week_offset)))[0]

    return JSONResponse(week.json(cal))


@login_required
def move_entry(request, entry_id, jsdate):
    e = get_object_or_404(models.Entry, pk=int(entry_id))
    e.entry_date = datetime.datetime.utcfromtimestamp(int(jsdate)/1000.0)
    e.save()

    return JSONResponse("ok")

@login_required
def set_workout_type(request, entry_id, workout_type):
    e = get_object_or_404(models.Entry, pk=int(entry_id))
    e.workout_type = workout_type
    e.save()
    return entry(request, entry_id)

@login_required
def entry(request, entry_id):
    e = get_object_or_404(models.Entry, pk=int(entry_id))
    return JSONResponse(e.json())

def workout_summary(request, user_id):
    workouts = models.StravaActivity.objects.filter(user=int(user_id)).order_by('-start_datetime_local')[:1000]
    data = [w.json() for w in workouts]
    return JSONResponse(data)

def activity_streams(request, activity_id):
    a = models.StravaActivity.objects.filter(activity_id=activity_id)
    streams = models.StravaActivityStream.objects.filter(activity=a).order_by('time')
    return JSONResponse([x.json() for x in streams])

def activity_curves(request, activity_id):
    a = models.StravaActivity.objects.filter(activity_id=activity_id)
    pc = models.StravaPowerCurve.objects.filter(activity=a).order_by('interval_length')
    ps = models.StravaSpeedCurve.objects.filter(activity=a).order_by('interval_length')

    d2 = pytz.timezone('US/Central').localize(datetime.datetime.now())
    d1 = d2 - datetime.timedelta(days=7*6)

    from django.db import connection

    curves = {
        'watts': {int(x.interval_length): x.watts for x in pc},
        'speed': {int(x.interval_length): x.speed_mph for x in ps},
        'watts_min': {},
        'watts_max': {},
        'speed_min': {},
        'speed_max': {},
    }

    c = connection.cursor()

    query = """
        select interval_length, max(watts) as max_watts, min(watts) as min_watts
        from bikecal_stravapowercurve c
        join bikecal_stravaactivity a using (activity_id)
        where a.start_datetime_local between '{d1}' and '{d2}'
        group by c.interval_length
        order by c.interval_length
    """.format(
        d1 = d1.strftime("%Y-%m-%d %H:%M:%S"),
        d2 = d2.strftime("%Y-%m-%d %H:%M:%S"),
    )
    c.execute(query)
    while True:
        row = c.fetchone()
        logger.warn("row == %r", row)
        if not row:
            break
            
        curves['watts_max'][row[0]] = row[1]
        curves['watts_min'][row[0]] = row[2]
    

    query = """
        select interval_length, max(speed) as max, min(speed) as min
        from bikecal_stravaspeedcurve c
        join bikecal_stravaactivity a using (activity_id)
        where a.start_datetime_local between '{d1}' and '{d2}'
        group by c.interval_length
        order by c.interval_length
    """.format(
        d1 = d1.strftime("%Y-%m-%d %H:%M:%S"),
        d2 = d2.strftime("%Y-%m-%d %H:%M:%S"),
    )
    c.execute(query)
    while True:
        row = c.fetchone()
        logger.warn("row == %r", row)
        if not row:
            break
            
        curves['speed_max'][row[0]] = (row[1] / 1609.34)*3600
        curves['speed_min'][row[0]] = (row[2] / 1609.34)*3600
        
    return JSONResponse(curves)

def zones(request, user_id):
    cal = models.Calendar(user=user_id, all=request.REQUEST.get('all', False))
    
    zones = ["1", "2", "3", "4", "5a", "5b", "5c", "6"]
    data = {z: {'hr': cal.season.zone_hr(z), 'power': cal.season.zone_power(z)} for z in zones}
    return JSONResponse(data)

