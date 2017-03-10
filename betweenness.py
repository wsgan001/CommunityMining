#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 15:07:36 2017

@author: zhangchi
"""

from heapq import heappush, heappop
from itertools import count
import networkx as nx
import random

def single_source_shortest_path_basic(G, s):
    S = []
    P = {}
    for v in G:
        P[v] = []
    sigma = dict.fromkeys(G, 0.0)    # sigma[v]=0 for v in G
    D = {}
    sigma[s] = 1.0
    D[s] = 0
    Q = [s]
    while Q:   # use BFS to find shortest paths
        v = Q.pop(0)
        S.append(v)
        Dv = D[v]
        sigmav = sigma[v]
        for w in G[v]:
            if w not in D:
                Q.append(w)
                D[w] = Dv + 1
            if D[w] == Dv + 1:   # this is a shortest path, count paths
                sigma[w] += sigmav
                P[w].append(v)  # predecessors
    return S, P, sigma
    
def accumulate_basic(betweenness, S, P, sigma, s):
    delta = dict.fromkeys(S, 0)
    while S:
        w = S.pop()
        coeff = (1.0 + delta[w]) / sigma[w]
        for v in P[w]:
            delta[v] += sigma[v] * coeff
        if w != s:
            betweenness[w] += delta[w]
    return betweenness
    
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
G.add_edge('e','f',weight=0.8)
G.add_edge('e','g',weight=0.8)
G.add_edge('e','h',weight=0.8)
G.add_edge('f','g',weight=0.8)
G.add_edge('f','h',weight=0.8)
G.add_edge('g','i',weight=0.8)
G.add_edge('h','i',weight=0.8)
G.add_edge('h','j',weight=0.8)
G.add_edge('b','k',weight=0.8)
G.add_edge('k','i',weight=0.8)

#betweenness = nx.betweenness_centrality(G)

S, P, sigma = single_source_shortest_path_basic(G,'a')
betweenness = dict.fromkeys(G, 0.0)
betweenness = accumulate_basic(betweenness,S, P, sigma,'a')
