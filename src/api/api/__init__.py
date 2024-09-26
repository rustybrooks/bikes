import datetime
import logging
import os

import api_framework  # type: ignore
import flask_login  # type: ignore
from api_framework import Api, api_int, api_register, HttpResponse
from flask import Flask, redirect, render_template
from flask_cors import CORS  # type: ignore

from api.api.calendar_api import Calendar, CalendarTemplateApi  # type: ignore
from api.api.users_api import Users
from api.api.utils import is_logged_in
from bikedb import heatmap, offroad, queries, stravaapi  # type: ignore

osmnx_cache_dir = '/srv/data/osmnx_cache'
if not os.path.exists(osmnx_cache_dir):
    os.makedirs(osmnx_cache_dir)

root = os.path.join(os.path.dirname(__file__))

logger = logging.getLogger(__name__)
app = Flask(
    'bikes-api',
    template_folder=os.path.join(root, 'templates'),
    static_folder=os.path.join(root, 'static')
)
CORS(app, origins=["http://localhost:5000", "http://localhost:3000", "bikes.rustybrooks.com"],
     supports_credentials=True, max_age=24 * 60 * 60)

app.secret_key = '60c5c072f919967af78b7acdc352ce34328d36df2a06e970d2d7ec905aa349df'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


@app.route('/health/')
def health():
    return 'so healthy'


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
        if not username or not password:
            return HttpResponse(render_template('login.html'))

        user = queries.User(username=username, password=password)
        if user.is_authenticated():
            flask_login.login_user(user)
        else:
            return HttpResponse(render_template('login.html'))

    @classmethod
    @Api.config(require_login=False)
    def signup(cls, username=None, password=None, password2=None):
        if not username or not password:
            return HttpResponse(render_template('signup.html'))

        if password != password2:
            raise Api.BadRequest("Passwords don't match")

        if len(password) < 8:
            raise Api.BadRequest("Password must be at least 8 characters")

        queries.add_user(username=username, password=password)

        # code to validate and add user to database goes here
        return redirect("/login")

    @classmethod
    def strava_connect(cls):
        authorize_url = stravaapi.redirect_token()
        r = redirect(authorize_url)
        hr = HttpResponse(content=r.response, status=r.status, content_type=r.content_type)
        hr.headers = r.headers
        return hr

    @classmethod
    def strava_callback(cls, code=None, state=None, _user=None):
        stravaapi.get_token(_user, code)
        r = redirect(state)
        hr = HttpResponse(content=r.response, status=r.status, content_type=r.content_type)
        hr.headers = r.headers
        return hr

    @classmethod
    def strava_refresh(cls, _user=None):
        stravaapi.refresh_token(_user)
        return {}

    @classmethod
    def strava_update(cls, _user=None, days_ago=60):
        stravaapi.activities_sync_many(_user, days_ago=api_int(days_ago))
        return "done"

    @classmethod
    @Api.config(require_login=is_logged_in)
    def test(cls, strava_activity_id=None):
        fn = offroad.find_offroad_segments(strava_activity_id or 2347770699, do_graph=True)
        resp = HttpResponse(
            content=open(fn, 'rb').read(),
            content_type='image/png',
        )
        os.unlink(fn)
        return resp

    @classmethod
    @Api.config(require_login=is_logged_in)
    def heatmap(cls):
        fn = heatmap.generate(
            type='Ride', start_date=datetime.datetime(2018, 1, 1),
        )
        resp = HttpResponse(
            content=open(fn, 'rb').read(),
            content_type='image/png',
        )
        os.unlink(fn)
        return resp


api_framework.app_class_proxy(app, '', '/', Interface())
api_framework.app_class_proxy(app, '', '/calendar', CalendarTemplateApi())
api_framework.app_class_proxy(app, '', '/api/calendar', Calendar())
api_framework.app_class_proxy(app, '', '/api/users', Users())

api_framework.app_class_proxy(
    app, "", "api/framework", api_framework.FrameworkApi()
)

codes = [400, 406, 404]

for code in codes:
    app.register_error_handler(code, lambda e: e.get_response())

# if os.getenv('ENVIRONMENT') != 'prod':
#    app.register_error_handler(500, lambda e: str(e))
