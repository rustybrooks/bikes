import matplotlib

matplotlib.use('Agg')
import osmnx as ox
import matplotlib.pyplot as plt
import numpy as np

import datetime
from flask import Flask, request, render_template, session, redirect, url_for, escape
import logging
import os
import tempfile
import time

from lib import api_framework, config
from lib.api_framework import api_register, Api, HttpResponse, api_bool
from flask_cors import CORS
import flask_login

osmnx_cache_dir = '/srv/data/osmnx_cache'
if not os.path.exists(osmnx_cache_dir):
    os.makedirs(osmnx_cache_dir)

ox.utils.config(
    # data_folder='data',
    # logs_folder='logs',
    # imgs_folder='images',
    cache_folder=osmnx_cache_dir,
    use_cache=True,
    # log_file=False,
    # log_console=False,
    # log_level=20,
    # log_name='osmnx',
    # log_filename='osmnx',
    # useful_tags_node=['ref', 'highway'],
    # useful_tags_path=['bridge', 'tunnel', 'oneway', 'lanes', 'ref', 'name', 'highway', 'maxspeed', 'service', 'access', 'area', 'landuse', 'width', 'est_width', 'junction'],
    # osm_xml_node_attrs=['id', 'timestamp', 'uid', 'user', 'version', 'changeset', 'lat', 'lon'],
    # osm_xml_node_tags=['highway'],
    # osm_xml_way_attrs=['id', 'timestamp', 'uid', 'user', 'version', 'changeset'],
    # osm_xml_way_tags=['highway', 'lanes', 'maxspeed', 'name', 'oneway'],
    # default_access='["access"!~"private"]',
    # default_crs='+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs',
    # default_user_agent='Python OSMnx package (https://github.com/gboeing/osmnx)',
    # default_referer='Python OSMnx package (https://github.com/gboeing/osmnx)',
    # default_accept_language='en'
)


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
        stravaapi.get_token(_user, code)
        r = redirect(state)
        return HttpResponse(content=r.response, status=r.status, content_type=r.content_type, headers=r.headers)

    @classmethod
    def strava_refresh(cls, _user=None):
        stravaapi.refresh_token(_user)
        return {}

    @classmethod
    def strava_update(cls, _user=None):
        stravaapi.activities_sync_many(_user, days_ago=60)
        return "done"

    @classmethod
    def _point_to_line_dist(cls, point, line):
        """Calculate the distance between a point and a line segment.

        To calculate the closest distance to a line segment, we first need to check
        if the point projects onto the line segment.  If it does, then we calculate
        the orthogonal distance from the point to the line.
        If the point does not project to the line segment, we calculate the
        distance to both endpoints and take the shortest distance.

        :param point: Numpy array of form [x,y], describing the point.
        :type point: numpy.core.multiarray.ndarray
        :param line: list of endpoint arrays of form [P1, P2]
        :type line: list of numpy.core.multiarray.ndarray
        :return: The minimum distance to a point.
        :rtype: float
        """
        # unit vector
        unit_line = line[1] - line[0]
        norm_unit_line = unit_line / np.linalg.norm(unit_line)

        # compute the perpendicular distance to the theoretical infinite line
        segment_dist = (
            np.linalg.norm(np.cross(line[1] - line[0], line[0] - point)) /
            np.linalg.norm(unit_line)
        )

        diff = (
            (norm_unit_line[0] * (point[0] - line[0][0])) +
            (norm_unit_line[1] * (point[1] - line[0][1]))
        )

        x_seg = (norm_unit_line[0] * diff) + line[0][0]
        y_seg = (norm_unit_line[1] * diff) + line[0][1]

        endpoint_dist = min(
            np.linalg.norm(line[0] - point),
            np.linalg.norm(line[1] - point)
        )

        # decide if the intersection point falls on the line segment
        lp1_x = line[0][0]  # line point 1 x
        lp1_y = line[0][1]  # line point 1 y
        lp2_x = line[1][0]  # line point 2 x
        lp2_y = line[1][1]  # line point 2 y
        is_betw_x = lp1_x <= x_seg <= lp2_x or lp2_x <= x_seg <= lp1_x
        is_betw_y = lp1_y <= y_seg <= lp2_y or lp2_y <= y_seg <= lp1_y
        if is_betw_x and is_betw_y:
            return segment_dist
        else:
            # if not, then return the minimum distance to the segment endpoints
            return endpoint_dist

    @classmethod
    def _dist_pt_to_seg(cls, p, seg):
        import math

        def dis(latA, lonA, latB, lonB):
            R = 6371000
            return math.acos(math.sin(latA) * math.sin(latB) + math.cos(latA) * math.cos(latB) * math.cos(lonB - lonA)) * R

        def bear(latA, lonA, latB, lonB):
            return math.atan2(math.sin(lonB - lonA) * math.cos(latB), math.cos(latA) * math.sin(latB) - math.sin(latA) * math.cos(latB) * math.cos(lonB - lonA) )

        lat1, lon1 = seg[0]
        lat2, lon2 = seg[1]
        lat3, lon3 = p

        lat1 = math.radians(lat1)
        lat2 = math.radians(lat2)
        lat3 = math.radians(lat3)
        lon1 = math.radians(lon1)
        lon2 = math.radians(lon2)
        lon3 = math.radians(lon3)

        R = 6371000.  # Earth's radius in meters

        bear12 = bear(lat1, lon1, lat2, lon2)
        bear13 = bear(lat1, lon1, lat3, lon3)
        dis13 = dis(lat1, lon1, lat3, lon3)

        if abs(bear13 - bear12) > (math.pi / 2.):
            dxa = dis13
        else:
            dxt = math.asin(math.sin(dis13 / R) * math.sin(bear13 - bear12)) * R

            dis12 = dis(lat1, lon1, lat2, lon2)
            dis14 = math.acos(math.cos(dis13 / R) / math.cos(dxt / R)) * R
            if dis14 > dis12:
                dxa = dis(lat2, lon2, lat3, lon3)
            else:
                dxa = abs(dxt)

        return dxa

    @classmethod
    def _dist(cls, origin, destination):
        import math

        lat1, lon1 = origin
        lat2, lon2 = destination
        radius = 6371  # km

        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) * math.sin(dlon / 2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = radius * c
        return d

#    @classmethod
#    def delete_all(cls):
#        for table in [
#            'speed_curves', 'power_curves', 'strava_activity_streams',
#            'strava_activity_segment_effort_achs', 'strava_activity_segment_effort',
#            'strava_segments', 'strava_activities'
#
#        ]
#            queries.SQL.delete(table)



    @classmethod
    @Api.config(require_login=is_logged_in)
    def test(cls):
        # importing libraries
        import pandas as pd  # Reading csv file
        from shapely.geometry import Point, LineString  # Shapely for converting latitude/longtitude to geometry
        import geopandas as gpd  # To create GeodataFrame

        t1 = time.time()
        data = queries.activity_streams(strava_activity_id=2347770699, sort='time')

#        route = gpd.GeoDataFrame(crs={'init': 'epsg:4326'}, geometry=[
#            LineString([(a.long, a.lat), (b.long, b.lat)]) for a, b in zip(data[:-1], data[1:])
#        ])
        route = gpd.GeoDataFrame(crs={'init': 'epsg:4326'}, geometry=[
            Point((a.long, a.lat)) for a in data
        ])

        # gdf_projected = gdf.to_crs('utm')

        north = max([x.lat for x in data])
        south = min([x.lat for x in data])
        east = max([x.long for x in data])
        west = min([x.long for x in data])

        t2 = time.time()
        G = ox.graph_from_bbox(
            north, south, east, west,
            truncate_by_edge=True, simplify=True, clean_periphery=False, network_type='all'
        )
        t3 = time.time()
        G_p = ox.project_graph(G)
        t4 = time.time()

#        buildings = ox.create_footprints_gdf(north=north, south=south, east=east, west=west, footprint_type='building')
#         areas = ox.create_footprints_gdf(north=north, south=south, east=east, west=west, footprint_type='place')
        nodes_p, edges_p = ox.graph_to_gdfs(G_p, nodes=True, edges=True)

        t4a = time.time()
        buildings_p = ox.project_gdf(buildings)
        # nodes_p = ox.project_gdf(nodes)
#        edges_p = ox.project_gdf(edges)
        route_p = ox.project_gdf(route)

        t5 = time.time()
        logger.warn("%r - %r", len(nodes_p), len(edges_p))

        geom = route_p['geometry']
        logger.warn(".....")
        X = [x.x for x in geom]
        Y = [x.y for x in geom]
        # logger.warn("X=%r, Y=%r", X, Y)
        e = ox.get_nearest_edges(G_p, X=X, Y=Y, method='kdtree', dist=1)
        logger.warn("after nearest")
        t6 = time.time()

        logger.warn("e = %r", e[0])

        pts = []
        for x, d in zip(e, geom):
            # e = edges.loc[x]
#            logger.warn("e = %r %r", e, dir(e))
#            logger.warn("x = %r", x.__class__)
            n1 = nodes_p.loc[x[0]]
            n2 = nodes_p.loc[x[1]]
            # logger.warn("%r %r", n1.x, n1.y)
#            logger.warn("%r", cls._dist((n1.x, n1.y), (n2.x, n2.y)))
            p = np.array((d.x, d.y))
            seg = [
                np.array((n1.x, n1.y)),
                np.array((n2.x, n2.y))
            ]
            dist = cls._point_to_line_dist(p, seg)
            # logger.warn("%r", dist)
            if (dist > 20):
                pts.append(p)
        offroad_p = gpd.GeoDataFrame(crs={'init': 'espg:4326'}, geometry=[Point(p) for p in pts])
        # offroad_p = ox.project_gdf(offroad)
        t7 = time.time()

        with tempfile.NamedTemporaryFile(mode="w+b", suffix='.png') as tf:
            fig, ax = plt.subplots(figsize=(12,12))
            ax.set_aspect('equal')

            # area.plot(ax=ax, facecolor='black')
            # areas_p.plot(ax=ax, edgecolor='purple', facecolor='pink')
            edges_p.plot(ax=ax, linewidth=1, edgecolor='#BC8F8F')
            buildings_p.plot(ax=ax, facecolor='#eeeeee', alpha=1)
            route_p.plot(ax=ax, alpha=0.5, linewidth=1, markersize=1, color='red')
            offroad_p.plot(ax=ax, alpha=1, markersize=1, color='green')
            plt.tight_layout()
            plt.axis('off')
            plt.subplots_adjust(hspace=0, wspace=0, left=0, top=1, right=1, bottom=0)
            plt.savefig(tf.name, dpi=300)

            te = time.time()
            logger.warn("%0.3f %0.3f %0.3f %0.3f %0.3f %0.3f %0.3f %0.3f", t2-t1, t3-t2, t4-t3, t4a-t4, t5-t4a, t6-t5, t7-t6, te-t7)

            return HttpResponse(
                content=open(tf.name, 'rb').read(),
                content_type='image/png',
            )



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
