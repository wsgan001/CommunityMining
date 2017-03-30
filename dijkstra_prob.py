#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 00:26:34 2017

@author: zhangchi
"""

from heapq import heappush, heappop
from itertools import count
import networkx as nx

def single_source_dijkstra_path_length(G, source, cutoff=None, beta=0.5, weight='weight'):
    get_weight = lambda u, v, data: data.get(weight, 1)
    if cutoff is not None:
        cutoff = -cutoff
    return _dijkstra(G, source, get_weight, cutoff=cutoff, beta=beta)
    
def _dijkstra(G, source, get_weight, cutoff=None, beta=0.5):
    G_succ = G.adj
    push = heappush
    pop = heappop
    dist = {}  # dictionary of final distances
    seen = {source: -1}
    c = count()
    fringe = []  # use heapq with (distance,label) tuples
    push(fringe, (-1, next(c), source))
    while fringe:
        (d, _, v) = pop(fringe)
        if v in dist:
            continue  # already searched this node.
        dist[v] = d
        for u, e in G_succ[v].items():
            cost = get_weight(v, u, e)
            if cost is None:
                continue
            vu_dist = dist[v] * get_weight(v, u, e)
            if cutoff is not None:
                if vu_dist > cutoff:
                    continue
            if u in dist:
                if vu_dist < dist[u]:
                    raise ValueError('Contradictory paths found:','negative weights?')
            elif u not in seen or vu_dist < seen[u]:
                seen[u] = vu_dist
                push(fringe, (vu_dist, next(c), u))
    for item in dist:
        dist[item] *= -1
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
print single_source_dijkstra_path_length(G,'a',cutoff=0.75,beta=1)
'''
G.add_edge('a','c',weight=0.8)
G.add_edge('c','d',weight=0.7)
G.add_edge('b','d',weight=0.6)
G.add_edge('a','d',weight=0.5)
G.add_edge('b','c',weight=0.6)
G.add_edge('c','e',weight=0.7)
G.add_edge('d','e',weight=0.6)
G.add_edge('c','f',weight=0.5)
G.add_edge('d','f',weight=0.7)
G.add_edge('e','f',weight=0.6)
G.add_edge('e','g',weight=0.5)
G.add_edge('e','h',weight=0.4)
G.add_edge('f','g',weight=0.5)
G.add_edge('f','h',weight=0.6)
G.add_edge('g','i',weight=0.7)
G.add_edge('h','i',weight=0.8)
G.add_edge('h','j',weight=0.9)
G.add_edge('b','k',weight=0.3)
G.add_edge('k','i',weight=0.4)
'''

#==============================================================================
# def _dijkstra_2(G, source, get_weight, cutoff=None, beta=0.5):
#     G_succ = G.adj
#     push = heappush
#     pop = heappop
#     dist = {}  # dictionary of final distances
#     seen = {source: 1}
#     c = count()
#     fringe = []  # use heapq with (distance,label) tuples
#     push(fringe, (1, next(c), source))
#     while fringe:
#         (d, _, v) = pop(fringe)
#         dist[v] = d
#         for u, e in G_succ[v].items():
#             cost = get_weight(v, u, e)
#             if cost is None:
#                 continue
#             vu_dist = dist[v] * get_weight(v, u, e) * beta
#             if cutoff is not None:
#                 if vu_dist < cutoff:
#                     continue
#             if u not in seen or vu_dist > seen[u]:
#                 seen[u] = vu_dist
#                 push(fringe, (vu_dist, next(c), u))
#     return dist
#==============================================================================
