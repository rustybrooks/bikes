from collections import defaultdict
import copy
from flask import Flask, request, render_template, request
import logging
import os

from lib import api_framework, client, config
from lib.api_framework import api_register, Api, HttpResponse, api_bool
from flask_cors import CORS

root = os.path.join(os.path.dirname(__file__))

logger = logging.getLogger(__name__)
app = Flask('bikes-webapi', template_folder=os.path.join(root, 'templates'), static_folder=os.path.join(root, 'static'))
CORS(app)


# api_framework.app_class_proxy(app, '', 'api/interface', Interface())


codes = [400, 406, 404]

for code in codes:
    app.register_error_handler(code, lambda e: e.get_response())

#if os.getenv('ENVIRONMENT') != 'prod':
#    app.register_error_handler(500, lambda e: str(e))
