import datetime
import logging
import os
import time
import urllib.parse

import numpy
import pytz
import requests

from bikedb import queries
from sqllib.sql import dictobj
# from requests.adapters import HTTPAdapter
# from urllib3.util import Retry

logger = logging.getLogger(__name__)


client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')


# # Define the retry strategy
# retry_strategy = Retry(
#     total=10,  # Maximum number of retries
#     backoff_factor=30,
#     status_forcelist=[429],  # HTTP status codes to retry on
#     backoff_max=5*60,
# )
# # Create an HTTP adapter with the retry strategy and mount it to session
# adapter = HTTPAdapter(max_retries=retry_strategy)
#
# # Create a new session object
# session = requests.Session()
# session.mount('http://', adapter)
# session.mount('https://', adapter)


class NoAuthCode(Exception):
    def __init__(self, user):
        self.msg = "No authorization code stored for user %d" % user.user_id


class StravaError(Exception):
    def __init__(self, message, errors, code):
        self.message = message
        self.errors = errors
        self.code = code

    def __str__(self):
        return f"StravaError(message={self.message}, errors={self.errors}, code={self.code})"


def retry_request(url, max_seconds=300, status_forcelist=None, **kwargs):
    status_forcelist = status_forcelist or [429]
    # Make number of requests required
    start_time = time.time()
    sleeptime = 60
    while time.time() - start_time < max_seconds:
        try:
            response = requests.get(url, **kwargs)
            if response.status_code in status_forcelist:
                # Retry request
                sleeptime = min(sleeptime + 60, 300)
                logger.info("Sleeping %r for url %r (total=%0.1f)", sleeptime, url, time.time() - start_time)
                time.sleep(sleeptime)
                continue
            return response
        except requests.exceptions.ConnectionError:
            pass

    return None

def get_auth_code(user):
    if user.expires_at and user.expires_at <= datetime.datetime.utcnow():
        logger.warning("expires at %r now = %r", user.expires_at, datetime.datetime.utcnow())
        user.access_token = refresh_token(user)

    return user.access_token

    
def redirect_token(return_to_url='/'):
    if os.getenv('ENVIRONMENT', "dev") == "dev":
        redirect_uri = 'http://localhost:5000/strava_callback'
    else:
        redirect_uri = "https://bikes-api.prod.rustybrooks.net/strava_callback"

    authorize_url = 'https://www.strava.com/oauth/authorize'
    authorize_url += "?"
    authorize_url += urllib.parse.urlencode({
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'state': return_to_url,
        'scope': 'read_all,activity:read_all',
    })

    return authorize_url


def get_token(user, code):
    access_token_url = 'https://www.strava.com/oauth/token'
    access_token_data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
    }

    response = requests.post(
        url=access_token_url,
        data=access_token_data,
        headers={'Api-Key': str(client_id)}
    )

    data = response.json()
    queries.update_user(
        user_id=user.user_id,
        access_token=data['access_token'],
        refresh_token=data['refresh_token'],
        expires_at=datetime.datetime.utcfromtimestamp(data['expires_at']),
    )

    return data['access_token']


def refresh_token(user):
    access_token_url = 'https://www.strava.com/oauth/token'
    access_token_data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'refresh_token',
        'refresh_token': user.refresh_token
    }

    response = requests.post(
        url=access_token_url,
        data=access_token_data,
        headers={'Api-Key': str(client_id)}
    )

    data = response.json()
    queries.update_user(
        user_id=user.user_id,
        access_token=data['access_token'],
        refresh_token=data['refresh_token'],
        expires_at=datetime.datetime.utcfromtimestamp(data['expires_at']),
    )


    return data['access_token']


def build_url(pieces):
    url = 'https://www.strava.com/api/v3'
    for p in pieces:
        url += "/" + p

    return url


def strava_fetch(user, url, **kwargs):
    url_args = ("?" + urllib.parse.urlencode(kwargs)) if len(kwargs) else ''
    full_url = url + url_args
    headers = {'api-key': str(client_id), 'authorization': 'Bearer %s' % get_auth_code(user)}
    # logger.warning("fetch url=%r, headers=%r", full_url, headers)
    response = retry_request(url=full_url, verify=True, headers=headers, max_seconds=60*60*24)
    ourjson = response.json()

    if isinstance(ourjson, dict) and 'errors' in ourjson:
        raise StravaError(
            message=ourjson['message'],
            errors=ourjson['errors'],
            code=response.status_code,
        )

    return ourjson


def self(user):
    url = build_url(['athlete'])
    return strava_fetch(user, url)


def get_activities(user, after=None, before=None, page=1, per_page=100):
    url = build_url(['athlete', 'activities'])
    kwargs = {}
    if after is not None:
        kwargs['after'] = int(after.strftime("%s"))
    if before is not None:
        kwargs['before'] = int(before.strftime("%s"))
    if page is not None:
        kwargs['page'] = page

    kwargs['per_page'] = per_page or 1

    while True:
        acts = strava_fetch(user, url, **kwargs)
        if not acts:
            break

        for a in acts:
            yield a

        kwargs['page'] += 1


def get_activity(user, activity_id):
    url = build_url(['activities', str(activity_id)])
    return strava_fetch(user, url, include_all_efforts=True)


def get_activity_stream(user, activity_id):
    types = 'time,latlng,distance,altitude,velocity_smooth,heartrate,cadence,watts,temp,moving,grade_smooth'
    url = build_url(['activities', str(activity_id), 'streams', types])

    try:
        return strava_fetch(user, url)
    except StravaError as e:
        if e.code == 404:
            return []

        raise e


def get_segment_leaderboard(user, segment_id):
    url = build_url(['segments', str(segment_id), 'leaderboard'])
    return strava_fetch(user, url)


#########################

def tznow():
    return pytz.utc.localize(datetime.datetime.utcnow())


@queries.SQL.is_transaction
def activities_sync_one(user, activity, full=False, rebuild=False):
    activity_id = activity['id']
    act = queries.activity(strava_activity_id=activity_id)

    # If we already have this one, let's not resync
    if act and not rebuild:
        return

    if 'segment_efforts' not in activity and full:
        return activities_sync_one(user, get_activity(user, activity['id']))

    logger.warning("Syncing activity %r", activity_id)

    new = not bool(act)
    if not act:
        act = dictobj()
        act.strava_activity_id = activity_id
        act.user_id = user.user_id

    for key in [
        'external_id', 'upload_id', 'distance', 'moving_time',
        'elapsed_time', 'total_elevation_gain', 'type', 'timezone',
        'achievement_count', 'athlete_count', 'trainer', 'commute', 'manual', 'private', 'embed_token',
        'workout_type', 'gear_id', 'average_speed', 'max_speed', 'average_cadence', 'average_temp', 'average_watts',
        'max_watts', 'weighted_average_watts', 'kilojoules', 'device_watts', 'average_heartrate', 'max_heartrate',
        'suffer_score', 'flagged'
    ]:
        act[key] = activity.get(key)

    act.activity_name = activity.get('name')

    act['elevation_high'] = activity.get('elev_high')
    act['elevation_low'] = activity.get('elev_low')
    act['athlete_id'] = activity['athlete']['id']

    act['start_datetime'] = activity['start_date']
    act['start_datetime_local'] = activity['start_date_local']

    act['start_lat'] = activity['start_latlng'][0] if activity['start_latlng'] else None
    act['start_long'] = activity['start_latlng'][1] if activity['start_latlng'] else None
    act['end_lat'] = activity['end_latlng'][0] if activity['end_latlng'] else None
    act['end_long'] = activity['end_latlng'][1] if activity['end_latlng'] else None

    if new:
        queries.add_activity(act)
    else:
        queries.update_activity(strava_activity_id=activity_id)

    if 'segment_efforts' in activity:
        for e in activity.get('segment_efforts', []):
            activity_segment_effort_sync_one(act, e)

    activity_stream_sync(user, act)

    return act


def activities_sync_many(user, days_ago=None):
    first_date = None
    if days_ago is not None:
        first_date = tznow() - datetime.timedelta(days=days_ago)

    for act in get_activities(user, after=first_date):
        activities_sync_one(user, act, full=True)


def activity_segment_effort_sync_one(activity, segment):
    segment_id = segment['id']
    sege = queries.activity_segment_effort(strava_segment_id=segment_id)
    new = not bool(sege)

    if not sege:
        sege = dictobj()
        sege.strava_segment_id = segment_id

    sege.strava_activity_id = activity.strava_activity_id
    sege.start_datetime = segment.get('start_date')
    sege.start_datetime_local = segment.get('start_date_local')

    for key in [
        'resource_state', 'name', 'elapsed_time', 'moving_time', 'distance', 'start_index', 'end_index',
        'average_cadence', 'average_watts', 'device_watts', 'average_heartrate', 'max_heartrate',
        'kom_rank', 'pr_rank', 'hidden'
    ]:
        setattr(sege, key, segment.get(key))

    segment_sync_one(segment['segment'])
    sege.strava_segment_id = segment['segment']['id']

    if new:
        i = queries.add_activity_segment_effort(sege)
        sege.strava_activity_segment_effort_id = i.strava_activity_segment_effort_id
    else:
        queries.update_activity_segment_effort(segment_id, sege)

    activity_segment_effort_ach_sync(sege, segment['achievements'])

    return sege


def segment_sync_one(segment):
    segment_id = segment['id']
    # logger.warning("Syncing segment %r", segment_id)
    seg = queries.segment(strava_segment_id=segment_id)
    new = not bool(seg)
    if not seg:
        seg = dictobj()
        seg.strava_segment_id = segment_id

    for key in [
        'resource_state', 'name', 'activity_type', 'distance', 'average_grade', 'maximum_grade', 'elevation_high',
        'elevation_low', 'climb_category', 'city', 'state',
        'country', 'private', 'starred', 'created_at', 'updated_at', 'total_elevation_gain', 'effort_count',
        'athlete_count', 'hazardous', 'star_count',
    ]:
        setattr(seg, key, segment.get(key))

    seg.start_lat = segment['start_latlng'][0] if segment['start_latlng'] else None
    seg.start_long = segment['start_latlng'][1] if segment['start_latlng'] else None
    seg.end_lat = segment['end_latlng'][0] if segment['end_latlng'] else None
    seg.end_long = segment['end_latlng'][1] if segment['end_latlng'] else None

    if new:
        queries.add_segment(seg)
    else:
        queries.update_segment(segment_id, seg)

    return seg


# Note, this actually downloads the data too, via the API
def activity_stream_sync(user, activity, force=False):
    t1 = time.time()
    logger.warning("Syncing activity stream id=%r", activity.strava_activity_id)
    current = queries.activity_streams(strava_activity_id=activity.strava_activity_id)
    if len(current) and not force:
        logger.warning("not len current and not force %r %r", len(current), force)
        return

    queries.delete_activity_streams(strava_activity_id=activity.strava_activity_id)

    stream_data = get_activity_stream(user, activity.strava_activity_id)
    if not stream_data:
        return

    types = []
    datas = []
    for stream in stream_data:
        types.append(stream['type'])
        datas.append(stream['data'])

    to_insert = []
    for datum in zip(*datas):
        s = dictobj()
        s.strava_activity_id = activity.strava_activity_id
        for t, d in zip(types, datum):
            if t == 'latlng':
                s.lat = d[0]
                s.long = d[1]
            else:
                setattr(s, t, d)

        to_insert.append(s.asdict())

    queries.add_activity_streams(to_insert)

    power_curve_process(activity.strava_activity_id)

    speed_curve_process(activity.strava_activity_id)
    logger.warning("Done with %r - took %0.2f", activity.strava_activity_id, time.time()-t1)


def activity_segment_effort_ach_sync(segment_effort, achievements):
    if not len(achievements):
        return

    queries.delete_activity_segment_effort_achs(
        strava_activity_segment_effort_id=segment_effort.strava_activity_segment_effort_id
    )
    for ach in achievements:
        a = dictobj()
        a.strava_activity_segment_effort_id = segment_effort.strava_activity_segment_effort_id
        a.type_id = ach['type_id']
        a.type = ach['type']
        a.rank = ach['rank']

        queries.add_activity_segment_effort_ach(a)


def power_curve_window(data, length):
    w = numpy.ones(length, 'd')
    x = numpy.array([a[1] for a in data])

    if len(w) > len(x):
        return 0

    s = x
    y = numpy.convolve(w / w.sum(), s, mode='same')
    return max(y)


def power_curve_process(activity_id, delete=False):
    existing = queries.power_curves(strava_activity_id=activity_id)
    if len(existing):
        if delete:
            existing.delete()
        else:
            return

    segments = []
    this_segment = []

    last = None
    first = None
    stream_data = queries.activity_streams(strava_activity_id=activity_id, sort='time')
    if not len(stream_data):
        logger.warning("No stream data for %d", activity_id)
        return

    logger.warning("Processing power curve for %d - %d", activity_id, len(stream_data))

    row = None
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
    max_seconds = min(row[0] - first, 20*60)
    intervals = list(range(1, 10, 1))
    intervals.extend(range(10, 5*60, 10))
    intervals.extend(range(5*60, 15*60, 30))
    intervals.extend(range(15*60, max_seconds, 60))
    curves = []
    for win in intervals:
        val = max([power_curve_window(s, win) for s in segments])
        if val == 0:
            continue

        p = dictobj()
        p.interval_length = win
        p.watts = float(val)
        p.strava_activity_id = activity_id
        curves.append(p.asdict())

    queries.add_power_curves(curves)


def speed_curve_window(data, length):
    if length >= len(data):
        return 0

    x = numpy.array([a[2] for a in data])
    tm = numpy.array([a[0] for a in data])
    distw = x[length:] - x[:-length]
    tmw = tm[length:] - tm[:-length]
    speed = distw / tmw
    return max(speed)


def speed_curve_process(activity_id, delete=False):
    existing = queries.speed_curves(strava_activity_id=activity_id)
    if len(existing):
        if delete:
            existing.delete()
        else:
            return

    segments = []
    this_segment = []

    stream_data = queries.activity_streams(strava_activity_id=activity_id, sort='time')
    if not len(stream_data):
        logger.warning("No stream data for %d", activity_id)
        return

    logger.warning("Processing speed curve for %d", activity_id)

    last = None
    first = None
    row = None
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
    intervals = list(range(1, 10, 1))
    intervals.extend(range(10, 5*60, 10))
    intervals.extend(range(5*60, 15*60, 30))
    intervals.extend(range(15*60, max_seconds, 60))

    curves = []
    for win in intervals:
        val = max([speed_curve_window(s, win) for s in segments])

        if val == 0:
            continue

#            logger.warning("Adding point %r", (activity_id_, interval_length, val)
        s = dictobj()
        s.interval_length = win
        s.speed = float(val)
        s.strava_activity_id = activity_id
        curves.append(s.asdict())

    queries.add_speed_curves(curves)
