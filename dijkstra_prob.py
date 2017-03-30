#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 00:26:34 2017

@author: zhangchi
"""

from heapq import heappush, heappop
#from itertools import count
import networkx as nx

def single_source_dijkstra_path_length(G, source, cutoff=None, weight='weight'):
    get_weight = lambda u, v, data: data.get(weight, 1)
    return _dijkstra(G, source, get_weight, cutoff=cutoff)
    
def _dijkstra(G, source, get_weight, cutoff=None):
    G_succ = G.succ if G.is_directed() else G.adj

    push = heappush
    pop = heappop
    dist = {}  # dictionary of final distances
    seen = {source: 1}
    #c = count()
    fringe = []  # use heapq with (distance,label) tuples
    push(fringe, (1, source))
    while fringe:
        (d, v) = pop(fringe)
        #if v in dist:
        #    continue  # already searched this node.
        dist[v] = d

        for u, e in G_succ[v].items():
            cost = get_weight(v, u, e)
            if cost is None:
                continue
            vu_dist = dist[v] * get_weight(v, u, e)
            if cutoff is not None:
                if vu_dist < cutoff:
                    continue
            if u in dist:
                if vu_dist > dist[u]:
                    dist[u] = vu_dist
                    #push(fringe, (vu_dist, next(c), u))
            #        raise ValueError('Contradictory paths found:','negative weights?')
            if u not in seen or vu_dist > seen[u]:
                seen[u] = vu_dist
                push(fringe, (vu_dist, u))

    return dist
    
G = nx.Graph()
G.add_edge('a','c',weight=0.95)
G.add_edge('c','d',weight=0.95)
G.add_edge('b','d',weight=0.8)
G.add_edge('a','d',weight=0.8)
G.add_edge('b','c',weight=0.65)
G.add_edge('c','e',weight=0.65)
G.add_edge('d','e',weight=0.8)
G.add_edge('c','f',weight=0.8)
G.add_edge('d','f',weight=0.8)
print single_source_dijkstra_path_length(G,'a')