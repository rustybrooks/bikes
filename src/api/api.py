from flask import Flask, render_template, redirect
import flask_login
import logging
import os

from lib import api_framework
from lib.api_framework import api_register, Api, HttpResponse, api_int
from flask_cors import CORS


osmnx_cache_dir = '/srv/data/osmnx_cache'
if not os.path.exists(osmnx_cache_dir):
    os.makedirs(osmnx_cache_dir)


from bikedb import queries, stravaapi, offroad


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
    def test(cls):
        fn = offroad.find_offroad_segments(2347770699, do_graph=True)
        resp = HttpResponse(
            content=open(fn, 'rb').read(),
            content_type='image/png',
        )
        os.unlink(fn)
        return resp


@api_register(None, require_login=is_logged_in)
class CalendarApi(Api):
    @classmethod
    def index(self):
        # cal = models.Calendar(user=request.user, all=request.REQUEST.get('all', False))
        #
        # script = bokeh.embed.autoload_server(
        #     model=None,
        #     app_path="/graphs/bike_weekly_summary",
        #     url="http://graphs-home.rustybrooks.com:5000/"
        # )

        context = {
            # 'calendar': cal,
            # 'reverse': reverse,
            # 'urllib': urllib,
            # 'datetime': datetime,
            # 'graph_script': script,
        }
        return HttpResponse(render_template('calendar/index.html'))


api_framework.app_class_proxy(app, '', '/', Interface())
api_framework.app_class_proxy(app, '', '/calendar', CalendarApi())


codes = [400, 406, 404]

for code in codes:
    app.register_error_handler(code, lambda e: e.get_response())

#if os.getenv('ENVIRONMENT') != 'prod':
#    app.register_error_handler(500, lambda e: str(e))
