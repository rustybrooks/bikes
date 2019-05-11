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

import pandas as pd  # Reading csv file
from shapely.geometry import Point, LineString  # Shapely for converting latitude/longtitude to geometry
import geopandas as gpd  # To create GeodataFrame

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



def get_nearest_edges(edges, X, Y, method=None, dist=0.0001):
    """
    Return the graph edges nearest to a list of points. Pass in points
    as separate vectors of X and Y coordinates. The 'kdtree' method
    is by far the fastest with large data sets, but only finds approximate
    nearest edges if working in unprojected coordinates like lat-lng (it
    precisely finds the nearest edge if working in projected coordinates).
    The 'balltree' method is second fastest with large data sets, but it
    is precise if working in unprojected coordinates like lat-lng.

    Parameters
    ----------
    G : networkx multidigraph
    X : list-like
        The vector of longitudes or x's for which we will find the nearest
        edge in the graph. For projected graphs, use the projected coordinates,
        usually in meters.
    Y : list-like
        The vector of latitudes or y's for which we will find the nearest
        edge in the graph. For projected graphs, use the projected coordinates,
        usually in meters.
    method : str {None, 'kdtree', 'balltree'}
        Which method to use for finding nearest edge to each point.
        If None, we manually find each edge one at a time using
        osmnx.utils.get_nearest_edge. If 'kdtree' we use
        scipy.spatial.cKDTree for very fast euclidean search. Recommended for
        projected graphs. If 'balltree', we use sklearn.neighbors.BallTree for
        fast haversine search. Recommended for unprojected graphs.

    dist : float
        spacing length along edges. Units are the same as the geom; Degrees for
        unprojected geometries and meters for projected geometries. The smaller
        the value, the more points are created.

    Returns
    -------
    ne : ndarray
        array of nearest edges represented by their startpoint and endpoint ids,
        u and v, the OSM ids of the nodes.

    Info
    ----
    The method creates equally distanced points along the edges of the network.
    Then, these points are used in a kdTree or BallTree search to identify which
    is nearest.Note that this method will not give the exact perpendicular point
    along the edge, but the smaller the *dist* parameter, the closer the solution
    will be.

    Code is adapted from an answer by JHuw from this original question:
    https://gis.stackexchange.com/questions/222315/geopandas-find-nearest-point
    -in-other-dataframe
    """
    # check if we were able to import scipy.spatial.cKDTree successfully
    if not ox.cKDTree:
        raise ImportError('The scipy package must be installed to use this optional feature.')

#    # transform graph into DataFrame
#    edges = ox.graph_to_gdfs(G, nodes=False, fill_edge_geometry=True)

    # transform edges into evenly spaced points
    edges['points'] = edges.apply(lambda x: ox.redistribute_vertices(x.geometry, dist), axis=1)

    # develop edges data for each created points
    extended = edges['points'].apply([ox.pd.Series]).stack().reset_index(level=1, drop=True).join(edges).reset_index()

    # Prepare btree arrays
    nbdata = np.array(list(zip(extended['Series'].apply(lambda x: x.x),
                               extended['Series'].apply(lambda x: x.y))))

    # build a k-d tree for euclidean nearest node search
    btree = ox.cKDTree(data=nbdata, compact_nodes=True, balanced_tree=True)

    # query the tree for nearest node to each point
    points = np.array([X, Y]).T
    dist, idx = btree.query(points, k=1)  # Returns ids of closest point
    logger.warn("dist1=%r", dist)
    eidx = extended.loc[idx, 'index']
    ne = edges.loc[eidx, ['u', 'v']]

    return dist, np.array(ne)



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
    @Api.config(require_login=is_logged_in)
    def test(cls):
        t1 = time.time()
        data = queries.activity_streams(strava_activity_id=2347770699, sort='time')

#        route = gpd.GeoDataFrame(crs={'init': 'epsg:4326'}, geometry=[
#            LineString([(a.long, a.lat), (b.long, b.lat)]) for a, b in zip(data[:-1], data[1:])
#        ])
        route_p = ox.project_gdf(gpd.GeoDataFrame(crs={'init': 'epsg:4326'}, geometry=[
            Point((a.long, a.lat)) for a in data
        ]))

        north = max([x.lat for x in data])
        south = min([x.lat for x in data])
        east = max([x.long for x in data])
        west = min([x.long for x in data])

        t2 = time.time()
        G_p = ox.project_graph(ox.graph_from_bbox(
            north, south, east, west,
            truncate_by_edge=True,
            simplify=True,
            clean_periphery=False,
            network_type='all'
        ))
        t3 = time.time()
        t4 = time.time()

        buildings_p = ox.project_gdf(ox.create_footprints_gdf(north=north, south=south, east=east, west=west, footprint_type='building'))
        # areas = ox.create_footprints_gdf(north=north, south=south, east=east, west=west, footprint_type='place')
        nodes_p, edges_p = ox.graph_to_gdfs(G_p, nodes=True, edges=True)

        t4a = time.time()
        t5 = time.time()
        logger.warn("%r - %r", len(nodes_p), len(edges_p))

        geom = route_p['geometry'][::1]
        logger.warn(".....")
        X = [x.x for x in geom]
        Y = [x.y for x in geom]
        # logger.warn("X=%r, Y=%r", X, Y)
        dists, edges = get_nearest_edges(edges_p, X=X, Y=Y, method='kdtree', dist=1)
        logger.warn("after nearest")
        t6 = time.time()

        pts = []
        for dist, g in zip(dists, geom):
            if (dist > 20):
                pts.append(g)

        offroad_p = gpd.GeoDataFrame(crs={'init': 'espg:4326'}, geometry=[Point(p) for p in pts])
        t7 = time.time()

        with tempfile.NamedTemporaryFile(mode="w+b", suffix='.png') as tf:
            fig, ax = plt.subplots(figsize=(12,12))
            ax.set_aspect('equal')

            # areas_p.plot(ax=ax, edgecolor='purple', facecolor='pink')
            edges_p.plot(ax=ax, linewidth=1, edgecolor='#BC8F8F')
            #nodes_p.plot(ax=ax, markersize=1, color='blue')
            buildings_p.plot(ax=ax, facecolor='#eeeeee', alpha=1)
            route_p.plot(ax=ax, alpha=0.25, linewidth=1, markersize=1, color='red')
            offroad_p.plot(ax=ax, alpha=.6, markersize=1, color='green')
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
