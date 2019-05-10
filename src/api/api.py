from collections import defaultdict
import copy
from flask import Flask, request, render_template, session, redirect, url_for, escape

import logging
import os

from lib import api_framework, config
from lib.api_framework import api_register, Api, HttpResponse, api_bool
from flask_cors import CORS
import flask_login

from bikedb.queries import User

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


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@api_register(None, require_login=False)
class Interface(Api):
    @classmethod
    def index(cls):
        return HttpResponse(render_template('index.html'))

    @classmethod
    def login(cls, username=None, password=None):
        # Here we use a class of some kind to represent and validate our
        # client-side form data. For example, WTForms is a library that will
        # handle this for us, and we use a custom LoginForm to validate.
        form = LoginForm()
        if form.validate_on_submit():
            # Login and validate the user.
            # user should be an instance of your `User` class
            flask_login.login_user(user)

            flask.flash('Logged in successfully.')

            next = flask.request.args.get('next')
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            if not is_safe_url(next):
                return flask.abort(400)

            return flask.redirect(next or flask.url_for('index'))
        return flask.render_template('login.html', form=form)

    @classmethod
    def stravacallback(cls):
        return {}


api_framework.app_class_proxy(app, '', '/', Interface())


codes = [400, 406, 404]

for code in codes:
    app.register_error_handler(code, lambda e: e.get_response())

#if os.getenv('ENVIRONMENT') != 'prod':
#    app.register_error_handler(500, lambda e: str(e))
