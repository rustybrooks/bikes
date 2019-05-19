#!/usr/bin/env python3

import matplotlib
matplotlib.use('Agg')

import datetime
import geopandas as gpd
from geopandas.plotting import plot_polygon_collection, plot_linestring_collection
import logging
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import osmnx as ox
import pandas as pd
import pickle
from shapely.geometry import Point, LineString
import shutil
import sys
import tempfile
import time


GRID_SIZE = 400.0

logger = logging.getLogger(__name__)

osmnx_cache_dir = '/srv/data/osmnx_cache'
if not os.path.exists(osmnx_cache_dir):
    os.makedirs(osmnx_cache_dir)


geom_cache_dir = '/srv/data/geom_cache'
if not os.path.exists(osmnx_cache_dir):
    os.makedirs(geom_cache_dir)

geom_mem_cache = {}


ox.utils.config(
    cache_folder=osmnx_cache_dir,
    use_cache=True,
)

root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root)

from bikedb import queries


counts = {}


def geom_loader(name, geom_key, generator):
    if name not in counts:
        counts[name] = {
            'load': 0,
            'generate': 0,
            'mem': 0,
        }

    key_str = ':'.join([str(x) for x in geom_key])

    memkey = "{}:{}".format(name, key_str)

    if memkey in geom_mem_cache:
        counts[name]['mem'] += 1
    else:
        dirname = os.path.join(geom_cache_dir, name)
        filename = os.path.join(dirname, key_str)
        if os.path.exists(filename):
            counts[name]['load'] += 1
            with open(filename, "rb") as f:
                data = pickle.load(f)
        else:
            counts[name]['generate'] += 1
            data = generator()
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            with open(filename, "w+b") as f:
                pickle.dump(data, f)

        geom_mem_cache[memkey] = data

    return geom_mem_cache[memkey]


def debounce_triggers(dists, triggers_off, triggers_on):
    last = 0
    segments = []
    for t in sorted(list(triggers_off) + list(triggers_on)):
        dist = dists[t] - dists[last]
        if dist < 50:
            if last == 0:
                pass
            else:
                if segments:
                    segments[-1][1] = t

            last = t
            continue

        if last == 0:
            on = t in triggers_off
        else:
            on = True if last in triggers_on else False

        color = 'on' if on else 'off'

        if segments and segments[-1][-1] == color:
            segments[-1][1] = t
        else:
            segment = [last, t, color]
            segments.append(segment)

        last = t

    if segments:
        segments.append(
            [last, -1, 'on' if segments[-1][2] == 'off' else 'on']
        )

    # print(segments)
    return segments


def get_nearest_edges(edges, geom, dist=0.0001):
    """
        this is a bastardized version of osmnx.get_nearest_edges, modified to only use kdtree and to return distances
    """
    X = [x.x for x in geom]
    Y = [x.y for x in geom]

    # check if we were able to import scipy.spatial.cKDTree successfully
    if not ox.cKDTree:
        raise ImportError('The scipy package must be installed to use this optional feature.')

    # transform edges into evenly spaced points
    edges['points'] = edges.apply(lambda x: ox.redistribute_vertices(x.geometry, dist), axis=1)

    # develop edges data for each created points
    extended = edges['points'].apply([pd.Series]).stack().reset_index(level=1, drop=True).join(edges).reset_index()

    # Prepare btree arrays
    nbdata = np.array(list(zip(extended['Series'].apply(lambda x: x.x),
                               extended['Series'].apply(lambda x: x.y))))

    # build a k-d tree for euclidean nearest node search
    btree = ox.cKDTree(data=nbdata, compact_nodes=True, balanced_tree=True)

    # query the tree for nearest node to each point
    points = np.array([X, Y]).T
    dist, idx = btree.query(points, k=1)  # Returns ids of closest point
    eidx = extended.loc[idx, 'index']
    ne = edges.loc[eidx, ['u', 'v']]

    return dist, np.array(ne)


def nearest_edges_kdtree(grid_key, crs, dist):
    edges = geom_loader('grid_edges', grid_key, lambda: load_grid_edges(grid_key[-2], grid_key[-1], crs))

    # transform edges into evenly spaced points
    edges['points'] = edges.apply(lambda x: ox.redistribute_vertices(x.geometry, dist), axis=1)

    # develop edges data for each created points
    extended = edges['points'].apply([pd.Series]).stack().reset_index(level=1, drop=True).join(edges).reset_index()

    # Prepare btree arrays
    nbdata = np.array(list(zip(extended['Series'].apply(lambda x: x.x),
                               extended['Series'].apply(lambda x: x.y))))

    # build a k-d tree for euclidean nearest node search
    return ox.cKDTree(data=nbdata, compact_nodes=True, balanced_tree=True)


def get_nearest_edges_sub(grid_key, geom, crs, dist=0.0001):
    """
        this is a bastardized version of osmnx.get_nearest_edges, modified to only use kdtree and to return distances
    """
    X = [x.x for x in geom]
    Y = [x.y for x in geom]

    # check if we were able to import scipy.spatial.cKDTree successfully
    if not ox.cKDTree:
        raise ImportError('The scipy package must be installed to use this optional feature.')

    btree = geom_loader('nearest_kdtree', grid_key, lambda: nearest_edges_kdtree(grid_key, crs, dist))

    # query the tree for nearest node to each point
    points = np.array([X, Y]).T
    dist, idx = btree.query(points, k=1)  # Returns ids of closest point
#    eidx = extended.loc[idx, 'index']
#    ne = edges.loc[eidx, ['u', 'v']]

    return dist, None


def load_grid_edges(grid_x, grid_y, crs):
    x1 = grid_x - GRID_SIZE / 2
    x2 = grid_x + GRID_SIZE + GRID_SIZE / 2
    y1 = grid_y - GRID_SIZE / 2
    y2 = grid_y + GRID_SIZE + GRID_SIZE / 2
    ls = LineString([
        [x1, y1],
        [x2, y1],
        [x2, y2],
        [x1, y2],
        [x1, y1],
    ])

    t = gpd.GeoDataFrame(geometry=[ls], crs=crs)
    tll = ox.project_gdf(t, to_latlong=True)
    west, south, east, north = tll.total_bounds

    try:
        tgp = ox.project_graph(ox.graph_from_bbox(
            north, south, east, west,
            truncate_by_edge=True, simplify=True, clean_periphery=False, network_type='all', retain_all=True
        ))
        tnp, tep = ox.graph_to_gdfs(tgp, nodes=True, edges=True)
        return tep
    except ox.core.EmptyOverpassResponse:
        pass

    return gpd.GeoDataFrame(geometry=[])


def find_offroad_segments(strava_activity_id, do_graph=False):
    segments = geom_loader('offroad_segments', (strava_activity_id, ), lambda: find_offroad_segments_internal(strava_activity_id))

    if do_graph:
        return graph_offroad_segments(strava_activity_id, segments)


def graph_offroad_segments(strava_activity_id, segments):
    data = queries.activity_streams(strava_activity_id=strava_activity_id, sort='time')
    if not len(data):
        return None

    route = gpd.GeoDataFrame(crs={'init': 'epsg:4326'}, geometry=[
        Point((a.long, a.lat)) for a in data
    ])
    west, south, east, north = route.total_bounds
    tgp = ox.graph_from_bbox(
        north, south, east, west,
        truncate_by_edge=True, simplify=True, clean_periphery=False, network_type='all', retain_all=True
    )
    tnp, edges = ox.graph_to_gdfs(tgp, nodes=True, edges=True)

    rg = []
    labels = []
    colors = []
    for p1, p2, l in segments:
        points = route['geometry'][p1:p2 + 1 if p2 > 0 else p2]
        if len(points) < 2:
            continue
        rg.append(LineString([(x.x, x.y) for x in points]))
        labels.append(l)
        if l == 'on':
            colors.append('red')
        elif l == 'off':
            colors.append('green')

    route_seg = gpd.GeoDataFrame(geometry=rg)
    route_seg['colors'] = colors

    with tempfile.NamedTemporaryFile(mode="w+b", suffix='.png', delete=False) as tf:
        name = tf.name
        fig, ax = plt.subplots(figsize=(12, 12))
        edges.plot(ax=ax, linewidth=1, edgecolor='#aaaaaa')
        plot_linestring_collection(ax, route_seg['geometry'], colors=route_seg['colors'], linewidth=1.5, alpha=0.5)

        plt.tight_layout()
        plt.axis('off')
        plt.subplots_adjust(hspace=0, wspace=0, left=0, top=1, right=1, bottom=0)
        plt.savefig(tf.name, dpi=300)

    return name


def find_offroad_segments_internal(strava_activity_id):
    thresh = 15

    data = queries.activity_streams(strava_activity_id=strava_activity_id, sort='time')
    if not len(data):
        return []

    route = gpd.GeoDataFrame(crs={'init': 'epsg:4326'}, geometry=[
        Point((a.long, a.lat)) for a in data
    ])
    route_p = ox.project_gdf(route)

    crs = route_p.crs
    zone = None
    for el in crs.split():
        if 'zone' in el:
            zone = el.split('=')[-1]

    lastkey = None
    geom = []
    dists = []
    for p in route_p['geometry']:
        grid_x = int(GRID_SIZE*math.floor(p.x/GRID_SIZE))
        grid_y = int(GRID_SIZE*math.floor(p.y/GRID_SIZE))
        key = (int(GRID_SIZE), zone, grid_x, grid_y)

        if key != lastkey:
            if geom:
                these_dists, edges = get_nearest_edges_sub(lastkey, geom, crs, dist=2)
                dists.extend(these_dists)
            geom = []

        geom.append(p)

        lastkey = key

    if geom:
        these_dists, edges = get_nearest_edges_sub(lastkey, geom, route_p.crs, dist=2)
        dists.extend(these_dists)

    dists = np.array(dists)

    d = np.array([(x.x, x.y) for x in route_p['geometry']])
    ed = np.append(np.linalg.norm(d[:-1]-d[1:], axis=1), 0)
    edc = ed.cumsum()
    route_p['each_dist'] = ed
    route_p['running_dist'] = edc

    triggers_on = np.flatnonzero((dists[:-1] >= thresh) & (dists[1:] < thresh))
    triggers_off = np.flatnonzero((dists[:-1] < thresh) & (dists[1:] >= thresh))
    segments = debounce_triggers(edc, triggers_off, triggers_on)

    return segments


if __name__ == '__main__':
    for x in queries.activities(type='Walk', start_datetime_after=datetime.datetime(2018, 1, 1), sort='start_datetime'):
        if not os.path.exists('/srv/data/graphs/'):
            os.makedirs('/srv/data/graphs')

        dst = '/srv/data/graphs/{}.png'.format(x.strava_activity_id)
        if os.path.exists(dst):
            continue

        logger.warn("%r - %r start -------------------------", x.strava_activity_id, x.start_datetime)
        t1 = time.time()
        name = find_offroad_segments(x.strava_activity_id, do_graph=True)
        t2 = time.time()
        if name:
            shutil.copy(name, dst)

        logger.warn("%r - %r took %0.1f -------------------------", x.strava_activity_id, x.start_datetime, t2-t1)
        for k in sorted(counts.keys()):
            for k2 in sorted(counts[k].keys()):
                logger.warn("%r - %r - %r", k, k2, counts[k][k2])
