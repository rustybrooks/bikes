import logging
import os
import requests
import urllib
import datetime

log = logging.getLogger(__name__)

if os.getenv('WEB_LOCAL', "0") == "1":
#    client_id = ""
#    client_secret = ""
    client_id = 'ey7t2ahjx97juha5d87ehp4e4ug2c7ce'
    client_secret = 'dNHJu2qg6eWM2yUxASPB6MxJSkwpUfvEKQkEeEjWCvq'
else:
    client_id = 'ey7t2ahjx97juha5d87ehp4e4ug2c7ce'
    client_secret = 'dNHJu2qg6eWM2yUxASPB6MxJSkwpUfvEKQkEeEjWCvq'

auth_codes = {}

class NoAuthCode(Exception):
    def __init__(self, user):
        self.msg = "No authorization code stored for user %d" % (user.id)

def get_auth_code(user):
    try:
        return auth_codes[user]
    except KeyError:
        log.warn("No auth code for %r", user)
        raise NoAuthCode(user)

def redirect_token(return_to_url):
    if os.getenv('WEB_LOCAL', "0") == "1":
        redirect_uri = 'http://localhost.mapmyapi.com:8000/mmfcallback'
    else:
        redirect_uri = "bike.rustybrooks.com/mmfcallback"
    authorize_url = 'https://www.mapmyfitness.com/v7.0/oauth2/authorize/'
    authorize_url += "?"
    authorize_url += urllib.urlencode({
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'state': return_to_url
    })

    return authorize_url

def refresh_token(access_token, user_id):
    refresh_token_url = 'https://oauth2-api.mapmyapi.com/v7.0/oauth2/access_token/'
    refresh_token_data = {
        'grant_type': 'refresh_token',
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': access_token['refresh_token']
    }

    response = requests.post(url=refresh_token_url,
                             data=refresh_token_data,
                             headers={'api-key': client_id, 'authorization': 'Bearer %s' % access_token}
                             )

    token = response.json()['access_token']
    auth_codes[user_id] = token

    return token

def get_token(code, user):
    access_token_url = 'https://api.mapmyfitness.com/v7.0/oauth2/access_token/'
    access_token_data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
    }

    response = requests.post(url=access_token_url,
                             data=access_token_data,
                             headers={'Api-Key': client_id}
                             )

    token = response.json()['access_token']
    log.info("Storing token for user %d" % user.id)
    auth_codes[user] = token

    return token

def build_url(pieces):
    url = 'https://oauth2-api.mapmyapi.com/v7.0/'
    for p in pieces:
        url += "/" + p

    return url

def mmf_fetch(user_obj, url, **kwargs):
    url_args = ("?" + urllib.urlencode(kwargs)) if len(kwargs) else ''
    full_url = url + url_args
    print full_url
    response = requests.get(url=full_url,
                            verify=False,
                            headers={'api-key': client_id, 'authorization': 'Bearer %s' % get_auth_code(user_obj)}
                            )
    return response.json()

def activity_type(user):
    url = build_url(['activity_type'])
    return mmf_fetch(user, url)

def self(user):
    url = build_url(['user', 'self'])
    return mmf_fetch(user, url)

def workout(user, **kwargs):
    workout_data = []
    url = build_url(['workout'])
    page_size = 40
    these_args = {
        'user': 5290880,
        'limit': page_size,
        'offset': 0,
    }
    these_args.update(kwargs)

    while True:
        this_data = mmf_fetch(user, url, **these_args)  # FIXME - add as user param or figure out somehow
        these_workouts = this_data['_embedded']['workouts']
        if not len(these_workouts):
            break
        workout_data.extend(these_workouts)
        these_args['offset'] += page_size

    return workout_data

def bodymass(user, **kwargs):
    import pytz
    bmdata = []
    url = build_url(['bodymass'])
    page_size = 40
    these_args = {
        'target_start_datetime': datetime.datetime(2016, 1, 1, tzinfo=pytz.utc).isoformat(),
        'limit': page_size,
        'offset': 0,
    }
    these_args.update(kwargs)

    while True:
        this_data = mmf_fetch(user, url, **these_args)
        log.warn("data=%r", this_data)
        return
