import calendar
import datetime
from flask import Flask, render_template, redirect
import flask_login
import logging
import os
import pytz

from lib import api_framework
from lib.api_framework import api_register, Api, HttpResponse, api_int, api_datetime
from flask_cors import CORS

from bikedb import queries, stravaapi, offroad, heatmap

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
        if not username or not password:
            return HttpResponse(render_template('login.html'))

        user = queries.User(username=username, password=password)
        if user.is_authenticated:
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
        return HttpResponse(content=r.response, status=r.status, content_type=r.content_type, headers=r.headers)

    @classmethod
    def strava_callback(cls, code=None, state=None, _user=None):
        stravaapi.get_token(_user, code)
        r = redirect(state)
        return HttpResponse(content=r.response, status=r.status, content_type=r.content_type, headers=r.headers)

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


def format_interval(duration):
    return str(datetime.timedelta(seconds=duration))


@api_register(None, require_login=is_logged_in)
class CalendarApi(Api):
    @classmethod
    def _fixdate(cls, d, tz):
        return pytz.utc.localize(d).astimezone(tz)

    @classmethod
    def index(cls, date=None, week_start_day=5, timezone='US/Central', _user=None):  # monday is 0, 5 is saturday etc
        tz = pytz.timezone(timezone)
        date = api_datetime(date) or cls._fixdate(datetime.datetime.utcnow(), tz)
        logger.warning("date=%r", date)

        cal = calendar.Calendar(week_start_day)
        weeks = cal.monthdatescalendar(date.year, date.month)
        first = weeks[0][0]
        last = weeks[-1][-1]

        first = tz.localize(datetime.datetime(first.year, first.month, first.day)).astimezone(pytz.utc)
        last = tz.localize(datetime.datetime(last.year, last.month, last.day)).astimezone(pytz.utc)

        # logger.warning("%r", cal.monthdatescalendar(date.year, date.month))
        logger.warning(
            "first=%r, last=%r",
            first.astimezone(pytz.utc),
            last.astimezone(pytz.utc) + datetime.timedelta(days=1)
        )

        activities = queries.activities(
            user_id=_user.user_id,
            start_datetime_after=first.astimezone(pytz.utc),
            start_datetime_before=last.astimezone(pytz.utc) + datetime.timedelta(days=1)
        )
        logger.warning("%r", activities[0])

        data = {}
        day_to_week = {}
        week_index = 0
        for w in weeks:
            logger.warning("w = %r", w)
            data['{}:totals'.format(week_index)] = {
                'moving_time': 0,
                'distance_mi': 0,
            }
            for d in w:
                day_to_week[d] = week_index
                data[d] = {
                    'activities': []
                }

            week_index += 1

        logger.warning("data keys = %r", data.keys())

        for a in activities:
            ad = cls._fixdate(a.start_datetime, tz).date()
            # ad = a.start_datetime

            logger.warning("%r - %r", ad, ad in data)
            data[ad]['activities'].append(a)
            data['{}:totals'.format(day_to_week[ad])]['distance_mi'] += a.distance_mi
            data['{}:totals'.format(day_to_week[ad])]['moving_time'] += a.moving_time

        return HttpResponse(render_template(
            'calendar/index.html', weeks=weeks, data=data, day_to_week=day_to_week, format_interval=format_interval
        ))


api_framework.app_class_proxy(app, '', '/', Interface())
api_framework.app_class_proxy(app, '', '/calendar', CalendarApi())

codes = [400, 406, 404]

for code in codes:
    app.register_error_handler(code, lambda e: e.get_response())

# if os.getenv('ENVIRONMENT') != 'prod':
#    app.register_error_handler(500, lambda e: str(e))
