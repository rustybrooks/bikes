import datetime
from flask import Flask, request, render_template, session, redirect, url_for, escape
import logging
import os
import time

from lib import api_framework, config
from lib.api_framework import api_register, Api, HttpResponse, api_bool
from flask_cors import CORS
import flask_login

from bikedb import queries, stravaapi

root = os.path.join(os.path.dirname(__file__))

logger = logging.getLogger(__name__)
app = Flask(
    'bikes-api',
    template_folder=os.path.join(root, 'templates'),
    static_folder=os.path.join(root, 'static')
)
CORS(app)

app.secret_key = '60c5c072f919967af78b7acdc352ce34328d36df2a06e970d2d7ec905aa349df'


login_manager = flask_login.LoginManager()
login_manager.init_app(app)


def is_logged_in(request, api_data, url_data):
    return flask_login.current_user


@login_manager.user_loader
def load_user(user_id):
    return queries.User(user_id=user_id, is_authenticated=True)


@api_register(None, require_login=is_logged_in)
class Interface(Api):
    @classmethod
    def index(cls):
        return HttpResponse(render_template('index.html'))

    @classmethod
    @Api.config(require_login=False)
    def login(cls, username=None, password=None):
        if username and password:
            user = queries.User(username=username, password=password)
            if user.is_authenticated:
                flask_login.login_user(user)
            else:
                return HttpResponse(render_template('login.html'))
        else:
            return HttpResponse(render_template('login.html'))

    @classmethod
    def strava_connect(cls):
        authorize_url = stravaapi.redirect_token()
        r = redirect(authorize_url)
        return HttpResponse(content=r.response, status=r.status, content_type=r.content_type, headers=r.headers)

    @classmethod
    def strava_callback(cls, code=None, state=None, _user=None):
        access_token, refresh_token, expires_at = stravaapi.get_token(code)
        logger.warn("access_token = %r, refresh_token = %r, expires_at = %r", access_token, refresh_token, expires_at)
        queries.update_user(
            user_id=_user.user_id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=datetime.datetime.utcfromtimestamp(expires_at),
        )
        r = redirect(state)
        return HttpResponse(content=r.response, status=r.status, content_type=r.content_type, headers=r.headers)

    @classmethod
    def strava_refresh(cls, _user=None):
        access_token, refresh_token, expires_at = stravaapi.refresh_token(_user)
        logger.warn("access_token = %r, refresh_token = %r, expires_at = %r", access_token, refresh_token, expires_at)
        queries.update_user(
            user_id=_user.user_id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=datetime.datetime.utcfromtimestamp(expires_at),
        )

        return "{} - {} - {}".format(access_token, refresh_token, expires_at)

    @classmethod
    def strava_update(cls, _user=None):
        stravaapi.activities_sync_many(_user)
        return "done"

    @classmethod
    @Api.config(require_login=is_logged_in)
    def test(cls):
        return "hi"


api_framework.app_class_proxy(app, '', '/', Interface())


codes = [400, 406, 404]

for code in codes:
    app.register_error_handler(code, lambda e: e.get_response())

#if os.getenv('ENVIRONMENT') != 'prod':
#    app.register_error_handler(500, lambda e: str(e))
