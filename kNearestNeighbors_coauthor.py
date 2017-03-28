#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 01:08:14 2017

@author: zhangchi
"""

import networkx as nx
import timeit

G = nx.random_partition_graph([100000],0.00009,0)
start = timeit.default_timer()
for i in range(10):
    result = nx.single_source_dijkstra_path_length(G,i,cutoff=2,weight='weight')
#Your statements here
stop = timeit.default_timer()
print stop - start