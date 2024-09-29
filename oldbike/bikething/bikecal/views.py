from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.shortcuts import get_object_or_404, redirect
from djangomako.shortcuts import render_to_response, render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import datetime
import logging
import re
import simplejson
import urllib

from . import models
from bikething import stravaapi

logger = logging.getLogger(__name__)

import bokeh.embed



@login_required
def update_entry(request, entry_id):
    entry = get_object_or_404(models.Entry, pk=entry_id)
    if 'workout_type' in request.GET:
        entry.workout_type = request.GET['workout_type']

    if 'increase_date' in request.GET:
        new_date = entry.entry_date + datetime.timedelta(days=int(request.GET['increase_date']))
        diff = (new_date - entry.week.week_start_date).days
        if diff >= 0 and diff < 7:
            entry.entry_date = new_date

    entry.save()
    return HttpResponseRedirect(reverse('calendar_index'))

@login_required
def reset_week(request, week_id):
    week = get_object_or_404(models.Week, pk=week_id)
    week.populate_entries(delete_first=True)

    return HttpResponseRedirect(reverse('calendar_index'))

@login_required
def summary(request):
    #seasons = models.Season.objects.filter(user=request.user).order_by('season_start_date')

    workouts = models.StravaActivity.objects.filter(user=request.user).order_by('-start_datetime_local')[:1000]

    context = {
        'workouts': workouts,
    }
    return render_to_response("bikecal/summary.html", context)


@login_required
def graph_cumulative(request):
    seasons = models.Season.objects.filter(user=request.user)

    #allkeys = set()
    time_data = {}
    for season in seasons:
        workouts = season.workouts()
        time_data[season] = {}
        cum = 0
        for key in sorted(workouts.keys()):
            for w in workouts[key]:
                cum += w.moving_time

            offset = (key - season.season_start_date).days
            time_data[season][offset] = cum
            #allkeys.add(offset)

    allkeys = range(366)

    series_data = []
    for season in seasons:
        last = 0
        time_data_list = []
        for key in sorted(allkeys):
            if key not in time_data[season]:
                time_data[season][key] = last

            last = time_data[season][key]
            time_data_list.append((int(last/(3600.0)*100))/100.0)

        series_data.append({
            'name': season.season_start_date.strftime("%Y-%m-%d"),
            'data': time_data_list,
        })

    context = {
        'seasons': seasons,
        'time_data': time_data,
        'allkeys': allkeys,
        'series': simplejson.dumps(series_data),
        'json_keys': simplejson.dumps(sorted(allkeys)),
        'graph_title': 'Cumulative Hours',
        'yaxis_label': 'Hours',
    }

    return render_to_response("bikecal/areagraph.html", context)

@login_required
def graph_weekly(request):
    from collections import defaultdict

    seasons = models.Season.objects.filter(user=request.user)
    allkeys = set()

    interval = request.REQUEST.get('interval', 'week')  # can also be... day?

    interval_lists = {}
    for season in seasons:
        interval_lists[season] = defaultdict(list)
        workouts = season.workouts()

        for key in workouts.keys():
            offset = (key - season.season_start_date).days
            print offset, offset / 7

            if interval == "week":
                timekey = int(offset/7)
            elif interval == "day":
                timekey = offset
            else:
                timekey = "foo"

            for w in workouts[key]:
                interval_lists[season][timekey].append((w.distance, w.moving_time))

            allkeys.add(timekey)


    series_data = []
    for season in seasons:
        time_data_list = []
        for key in sorted(allkeys):
            if key in interval_lists[season]:
                distance = sum([x[0] for x in interval_lists[season][key]]) / 1609.34
                moving_time = sum([x[1] for x in interval_lists[season][key]]) / 3600
                time_data_list.append(distance / float(moving_time))
            else:
                time_data_list.append(None)

        series_data.append({
            'name': season.season_start_date.strftime("%Y-%m-%d"),
            'data': time_data_list,
        })

    context = {
        'seasons': seasons,
        'allkeys': allkeys,
        'series': simplejson.dumps(series_data),
        'json_keys': simplejson.dumps(sorted(allkeys)),
        'graph_title': 'Speed per interval',
        'yaxis_label': 'Speed',
    }

    return render_to_response("bikecal/areagraph.html", context)


@login_required
def graph_power(request, rolling_window=7, interval_length=5):
    rolling_window = int(rolling_window)

    ymin = 1e12
    ymax = -1e12

    seasons = models.Season.objects.filter(user=request.user).order_by('season_start_date')

    series = []
    for season in seasons:
        this_series = []
        points = models.StravaPowerCurve.objects.filter(
            interval_length=int(interval_length)*60,
            activity__start_datetime_local__range=(season.season_start_date, season.season_end_date)
        ).order_by('activity__start_datetime_local')
        points = list(points.select_related())

        d = points[0].activity.start_datetime_local
        last = points[-1].activity.start_datetime_local
        while d <= last:
            d += datetime.timedelta(days=1)
            dx = d - datetime.timedelta(days=rolling_window)
            days = [a for a in points if a.activity.start_datetime_local>dx and a.activity.start_datetime_local<=d]
            if days:
                #strdate = "new Date.UTC(%d, %d, %d)" % (d.year, d.month-1, d.day)
                strdate = (d - points[0].activity.start_datetime_local).days
                m = max([val.watts for val in days])
                #m = sum([val.watts for val in days])/len([val.watts for val in days])
                if m < ymin:
                    ymin = m

                if m > ymax:
                    ymax = m

                this_series.append([strdate, m])

        series.append({
            'name': str(season),
            'data': this_series,
        })

    context = {
        'graph_title': 'Best Power (%d day window)' % (rolling_window, ),
        'series': simplejson.dumps(series),
        'yaxis_min': max(100, ymin),
        'yaxis_max': ymax,
    }

    return render_to_response("bikecal/linechart.html", context)


@login_required
def query(request):
    from django.db import connection
    if request.method == "POST":
        cursor = connection.cursor()

        cursor.execute(request.POST['query'])
        col_names = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()

        context = {
            'query': request.POST['query'],
            'data': data,
            'column_names': col_names,
        }
    else:
        context = {
            'query': '',
            'data': [],
            'column_names': [],
        }

    context.update({ "csrftoken": csrf(request)["csrf_token"] })

    return render_to_response("bikecal/query.html", context)

#@login_required
def activity(request, activity_id):
    activity = models.StravaActivity.objects.filter(activity_id=activity_id)[0]
    efforts = models.StravaActivitySegmentEffort.objects.filter(activity=activity).order_by('start_index')
    streams = models.StravaActivityStream.objects.filter(activity=activity)
    power_curve = models.StravaPowerCurve.objects.filter(activity=activity)
    speed_curve = models.StravaSpeedCurve.objects.filter(activity=activity)

    analysis_script = bokeh.embed.autoload_server(
        model=None,
        app_path="/graphs/bike_workout_analysis/",
        url="http://graphs-home.rustybrooks.com:6000",
    )
    analysis_script = re.sub(r'src=\"([^\"]*)\"', r'src="\1&activity_id={}"'.format(activity_id), analysis_script)

    curve_script = bokeh.embed.autoload_server(
        model=None,
        app_path="/graphs/bike_workout_curves/",
        url="http://graphs-home.rustybrooks.com:6000",
    )
    curve_script = re.sub(r'src=\"([^\"]*)\"', r'src="\1&activity_id={}"'.format(activity_id), curve_script)
    
    context = {
        'reverse': reverse,
        'activity': activity,
        'streams': streams,
        'efforts': efforts,
        'speed_curve': speed_curve,
        'power_curve': power_curve,
        'miles': lambda x: x/1609.34,
        'feet': lambda x: x*3.28084,
        'mph': lambda x: x*3600.0/1609.34,
        'analysis_script': analysis_script,
        'curve_script': curve_script,
    }
    return render_to_response("bikecal/activity.html", context)

@login_required
def activity_update_curves(request, activity_id):
    try:
        models.StravaPowerCurve.process_curve(activity_id, delete=True)
        models.StravaSpeedCurve.process_curve(activity_id, delete=True)
        return redirect('activity', activity_id=activity_id)
    except stravaapi.NoAuthCode:
        authorize_url = stravaapi.redirect_token(request.META['PATH_INFO'])
        return HttpResponseRedirect(authorize_url)


@login_required
def activity_update(request, activity_id):
    try:
        activity = models.StravaActivity.objects.filter(activity_id=activity_id)[0]
        models.StravaActivity.sync_one_byobj(request.user, activity)
        return redirect('activity', activity_id=activity.activity_id)
    except stravaapi.NoAuthCode:
        authorize_url = stravaapi.redirect_token(request.META['PATH_INFO'])
        return HttpResponseRedirect(authorize_url)


@login_required
def segment(request, segment_id):
    history = models.StravaSegmentHistory.objects.filter(segment_id=segment_id).order_by('-recorded_datetime')
    efforts = models.StravaActivitySegmentEffort.objects.filter(segment_id=segment_id).order_by('-start_datetime_local')
    context = {
        'history': history,
        'efforts': efforts,
    }
    return render_to_response("bikecal/segment.html", context)



