#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')

import osmnx as ox

G = ox.graph_from_point((37.79, -122.41), distance=750, network_type='all')
ox.plot_graph(G, save=True, show=False, filename='./test.png')
