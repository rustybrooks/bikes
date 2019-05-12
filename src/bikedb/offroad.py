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
    # ne = edges.loc[eidx, ['u', 'v']]

    return dist, None
#        , np.array(ne)


def find_offroad_segments(strava_activity_id, do_graph=False):
    data = queries.activity_streams(strava_activity_id=strava_activity_id, sort='time')

    logger.warn("1")
    route = gpd.GeoDataFrame(crs={'init': 'epsg:4326'}, geometry=[
        Point((a.long, a.lat)) for a in data
    ])
    route_p = ox.project_gdf(route)
    logger.warn("2")

    west, south, east, north = route.total_bounds
    G_p = ox.project_graph(ox.graph_from_bbox(
        north, south, east, west,
        truncate_by_edge=True, simplify=True, clean_periphery=False, network_type='all'
    ))
    logger.warn("3")

    nodes_p, edges_p = ox.graph_to_gdfs(G_p, nodes=True, edges=True)
    logger.warn("4")

    geom = route_p['geometry']
    dists, edges = get_nearest_edges(edges_p, geom, dist=2)
    offroad_p = gpd.GeoDataFrame(geometry=[Point(g) for d, g in zip(dists, geom) if d > 20])

    logger.warn("5")

    if do_graph:
        return graph_offroad_segments(route, route_p, edges_p, offroad_p)


def graph_offroad_segments(route, route_p, edges_p, offroad_p):
    # west, south, east, north = route.total_bounds
    # buildings_p = ox.project_gdf(ox.create_footprints_gdf(north=north, south=south, east=east, west=west, footprint_type='building'))

    with tempfile.NamedTemporaryFile(mode="w+b", suffix='.png', delete=False) as tf:
        name = tf.name
        fig, ax = plt.subplots(figsize=(12, 12))
        ax.set_aspect('equal')

        route_lp = gpd.GeoDataFrame(geometry=[
            LineString(x) for x in zip(route_p['geometry'][:-1], route_p['geometry'][1:])
        ])

        edges_p.plot(ax=ax, linewidth=1, edgecolor='#aaaaaa')
        # nodes_p.plot(ax=ax, markersize=1, color='blue')
        # buildings_p.plot(ax=ax, facecolor='#eeeeee', alpha=1)
        # route_p.plot(ax=ax, alpha=0.5, markersize=1, color='blue')
        route_lp.plot(ax=ax, alpha=0.5, linewidth=1.5, color='red')
        offroad_p.plot(ax=ax, alpha=.6, markersize=1, color='green')
        plt.tight_layout()
        plt.axis('off')
        plt.subplots_adjust(hspace=0, wspace=0, left=0, top=1, right=1, bottom=0)
        plt.savefig(tf.name, dpi=150)

    return name


if __name__ == '__main__':
    import cProfile
    import pstats

    if 'stats' in sys.argv:
        p = pstats.Stats('mystats')
        p.strip_dirs().sort_stats('cumulative').print_stats(25)
    else:
        cProfile.run('find_offroad_segments(2347770699, do_graph=True)', 'mystats')
