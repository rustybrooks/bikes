import datetime
import logging
import os
import pytz
import requests
import urllib.parse

from . import queries

logger = logging.getLogger(__name__)




class NoAuthCode(Exception):
    def __init__(self, user):
        self.msg = "No authorization code stored for user %d" % (user.id)


class StravaError(Exception):
    pass


def get_auth_code(user):
    return user.access_token

    
def redirect_token(return_to_url='/'):
    if os.getenv('ENVIRONMENT', "dev") == "dev":
        redirect_uri = 'http://localhost:5000/strava_callback'
    else:
        redirect_uri = "http://bike.rustybrooks.com/strava_callback"

    authorize_url = 'https://www.strava.com/oauth/authorize'
    authorize_url += "?"
    authorize_url += urllib.parse.urlencode({
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'state': return_to_url,
        'scope': 'read_all',
    })

    return authorize_url


def get_token(code):
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
    return data['access_token'], data['refresh_token'], data['expires_at']

    # token_obj = models.StravaTokens.objects.filter(user=user).first()
    # if token_obj:
    #     token_obj.auth_key = token
    # else:
    #     token_obj = models.StravaTokens()
    #     token_obj.user = user
    #     token_obj.auth_key = token
    #
    # token_obj.save()

    return token


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
    return data['access_token'], data['refresh_token'], data['expires_at']


def build_url(pieces):
    url = 'https://www.strava.com/api/v3'
    for p in pieces:
        url += "/" + p

    return url


def strava_fetch(user, url, **kwargs):
    url_args = ("?" + urllib.parse.urlencode(kwargs)) if len(kwargs) else ''
    full_url = url + url_args
    logger.info(full_url)
    response = requests.get(
        url=full_url,
        verify=False,
        headers={'api-key': str(client_id), 'authorization': 'Bearer %s' % get_auth_code(user)}
    )
    ourjson = response.json()

    if isinstance(ourjson, dict) and 'errors' in ourjson:
        raise StravaError(repr([ourjson['message']] + ourjson['errors']))

    return ourjson


def self(user):
    url = build_url(['athlete'])
    return strava_fetch(user, url)


def activities(user, after=None, before=None, page=None):
    url = build_url(['athlete', 'activities'])
    kwargs = {}
    if after is not None:
        kwargs['after'] = int(after.strftime("%s"))
    if before is not None:
        kwargs['before'] = int(before.strftime("%s"))
    if page is not None:
        kwargs['page'] = page
        kwargs['per_page'] = 200

    return strava_fetch(user, url, **kwargs)


def activity(user, activity_id):
    url = build_url(['activities', str(activity_id)])
    return strava_fetch(user, url, include_all_efforts=True)


def activity_stream(user, activity_id):
    types = 'time,latlng,distance,altitude,velocity_smooth,heartrate,cadence,watts,temp,moving,grade_smooth'
    url = build_url(['activities', str(activity_id), 'streams', types])
    return strava_fetch(user, url)


def segment_leaderboard(user, segment_id):
    url = build_url(['segments', str(segment_id), 'leaderboard'])
    return strava_fetch(user, url)


#########################

def tznow():
    return pytz.utc.localize(datetime.datetime.utcnow())


def activities_sync_one(user, activity, full=False, rebuild=False):
    activity_id = activity['id']
    act =
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


def activities_sync_many(user):
    first_date = tznow() - datetime.timedelta(days=14)

    for act in activities(user, after=first_date):
        activities_sync_one(user, act, full=True)
