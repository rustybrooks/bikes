import logging
import os
import requests
import urllib

# from . import models
from . import queries

logger = logging.getLogger(__name__)


client_id = 9981
client_secret = "95fffa4745f641a3eeae5d073ad870ce4680e37e"


class NoAuthCode(Exception):
    def __init__(self, user):
        self.msg = "No authorization code stored for user %d" % (user.id)


class StravaError(Exception):
    pass


def get_auth_code(user):
    try:
        token_obj = models.StravaTokens.objects.filter(user=user).first()
        logger.warn("token_obj = %r", token_obj)
        if not token_obj:
            raise NoAuthCode(user)

        return token_obj.auth_key
    except KeyError:
        raise NoAuthCode(user)

    
def redirect_token(return_to_url):
    if os.getenv('ENVIRONMENT', "dev") == "dev":
        redirect_uri = 'http://localhost:5000/stravacallback'
    else:
        redirect_uri = "http://bike.rustybrooks.com/stravacallback"

    authorize_url = 'https://www.strava.com/oauth/authorize'
    authorize_url += "?"
    authorize_url += urllib.urlencode({
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'state': return_to_url,
        'scope': 'read_all',
    })

    return authorize_url


def get_token(code, user):
    access_token_url = 'https://www.strava.com/oauth/token'
    access_token_data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
    }

    response = requests.post(
        url=access_token_url,
        data=access_token_data,
        headers={'Api-Key': client_id}
    )

    token = response.json()['access_token']

    token_obj = models.StravaTokens.objects.filter(user=user).first()
    if token_obj:
        token_obj.auth_key = token
    else:
        token_obj = models.StravaTokens()
        token_obj.user = user
        token_obj.auth_key = token

    token_obj.save()

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
        headers={'Api-Key': client_id}
    )

    token = response.json()['access_token']

    token_obj = models.StravaTokens.objects.filter(user=user).first()
    if token_obj:
        token_obj.auth_key = token
    else:
        token_obj = models.StravaTokens()
        token_obj.user = user
        token_obj.auth_key = token

    token_obj.save()

    return token


def build_url(pieces):
    url = 'https://www.strava.com/api/v3'
    for p in pieces:
        url += "/" + p

    return url


def strava_fetch(user_obj, url, **kwargs):
    url_args = ("?" + urllib.urlencode(kwargs)) if len(kwargs) else ''
    full_url = url + url_args
    logger.info(full_url)
    response = requests.get(url=full_url,
                            verify=False,
                            headers={'api-key': client_id, 'authorization': 'Bearer %s' % get_auth_code(user_obj)}
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
