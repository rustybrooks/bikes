#!/usr/bin/env python3

import matplotlib
matplotlib.use('Agg')

import geopandas as gpd
import logging
import matplotlib.pyplot as plt
import numpy as np
import os
import osmnx as ox
import pandas as pd
from shapely.geometry import Point, LineString
import sys
import tempfile
import time


logger = logging.getLogger(__name__)

osmnx_cache_dir = '/srv/data/osmnx_cache'
if not os.path.exists(osmnx_cache_dir):
    os.makedirs(osmnx_cache_dir)

ox.utils.config(
    cache_folder=osmnx_cache_dir,
    use_cache=True,
)

root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print(root)
sys.path.append(root)

from bikedb import queries


def debounce_triggers(dists, triggers_off, triggers_on):
    last = 0
    segments = []
    for t in sorted(list(triggers_off) + list(triggers_on)):
        dist = dists[t] - dists[last]
        if dist < 50:
            if last == 0:
                pass
            else:
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
            logger.warn("segment = %r", segment)
            segments.append(segment)

        last = t

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


def get_nearest_edges_sub(edges, geom, dist=0.0001):
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



def find_offroad_segments(strava_activity_id, do_graph=False):
    data = queries.activity_streams(strava_activity_id=strava_activity_id, sort='time')

    logger.warn("1")
    route = gpd.GeoDataFrame(crs={'init': 'epsg:4326'}, geometry=[
        Point((a.long, a.lat)) for a in data
    ])
    route_p = ox.project_gdf(route)

    d = np.array([(x.x, x.y) for x in route_p['geometry']])
    ed = np.append(np.linalg.norm(d[:-1]-d[1:], axis=1), 0)
    edc = ed.cumsum()
    route_p['each_dist'] = ed
    route_p['running_dist'] = edc
    # logger.warn("ed %r", ed)
    # logger.warn("running_dist %r", route_p['running_dist'])
    logger.warn("2")

    west, south, east, north = route.total_bounds
    G_p = ox.project_graph(ox.graph_from_bbox(
        north, south, east, west,
        truncate_by_edge=True, simplify=True, clean_periphery=False, network_type='all', retain_all=True
    ))
    logger.warn("3")

    nodes_p, edges_p = ox.graph_to_gdfs(G_p, nodes=True, edges=True)
    logger.warn("4")

    thresh = 15

    geom = route_p['geometry']
    dists, edges = get_nearest_edges(edges_p, geom, dist=2)
    # offroad_p = gpd.GeoDataFrame(geometry=[Point(g) for d, g in zip(dists, geom) if d > 20])
    # route_p['dist'] = dists
    # logger.warn("dists = %r", dists)
    # route_p['dist_w'] = [x for x in np.minimum(np.maximum(route_p['dist'], thresh), thresh).rolling(5, min_periods=0).max()]

    triggers_on = np.flatnonzero((dists[:-1] >= thresh) & (dists[1:] < thresh))
    triggers_off = np.flatnonzero((dists[:-1] < thresh) & (dists[1:] >= thresh))
    logger.warn("on = %r", triggers_on)
    logger.warn("off = %r", triggers_off)
    segments = debounce_triggers(edc, triggers_off, triggers_on)

    rg = []
    labels = []
    colors = []
    for p1, p2, l in segments:
        logger.warn("%r - %r - %r", p1, p2, len(route_p['geometry'][p1:p2+1]))
        rg.append(LineString([(x.x, x.y) for x in route_p['geometry'][p1:p2+1 if p2 > 0 else p2]]))
        labels.append(l)
        if l == 'on':
            colors.append('red')
        elif l == 'off':
            colors.append('green')
        elif l == 'deleted':
            colors.append('purple')

    route_seg_p = gpd.GeoDataFrame(geometry=rg)
    route_seg_p['colors'] = colors
    logger.warn('route_seg_p = %r', route_seg_p)

    logger.warn("5")

    if do_graph:
        return graph_offroad_segments(route, route_p, route_seg_p, edges_p)


def graph_offroad_segments(route, route_p, route_seg_p, edges_p):
    # west, south, east, north = route.total_bounds
    # buildings_p = ox.project_gdf(ox.create_footprints_gdf(north=north, south=south, east=east, west=west, footprint_type='building'))

    # route_lp = gpd.GeoDataFrame(
    #     geometry=[
    #         LineString(x) for x in zip(route_p['geometry'][:-1], route_p['geometry'][1:])
    #     ],
    # )
    # route_lp['dist_w'] = route_p['dist_w']

    with tempfile.NamedTemporaryFile(mode="w+b", suffix='.png', delete=False) as tf:
        name = tf.name
        fig, ax = plt.subplots(figsize=(12, 12))
        # ax.set_aspect('equal')

        edges_p.plot(ax=ax, linewidth=1, edgecolor='#aaaaaa')
        # nodes_p.plot(ax=ax, markersize=1, color='blue')
        # buildings_p.plot(ax=ax, facecolor='#eeeeee', alpha=1)
        # route_p.plot(ax=ax, alpha=0.5, markersize=1, column='dist_w', cmap='spring', scheme='equal_interval')
        # route_lp.plot(ax=ax, alpha=0.5, linewidth=2, column='dist_w', cmap='brg', scheme='equal_interval')
        # route_seg_p.plot(ax=ax, alpha=0.5, linewidth=2)
        from geopandas.plotting import plot_polygon_collection, plot_linestring_collection

        plot_linestring_collection(ax, route_seg_p['geometry'], colors=route_seg_p['colors'], linewidth=1.5, alpha=0.5)

        # offroad_p.plot(ax=ax, alpha=.6, markersize=1, color='green')
        plt.tight_layout()
        plt.axis('off')
        plt.subplots_adjust(hspace=0, wspace=0, left=0, top=1, right=1, bottom=0)
        plt.savefig(tf.name, dpi=400)

    return name


if __name__ == '__main__':
    import cProfile
    import pstats

    if 'stats' in sys.argv:
        p = pstats.Stats('mystats')
        p.strip_dirs().sort_stats('cumulative').print_stats(25)
    else:
        cProfile.run('find_offroad_segments(2347770699, do_graph=True)', 'mystats')
