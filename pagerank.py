#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 19:32:33 2017

@author: zhangchi
"""

import networkx as nx

G = nx.DiGraph()
G.add_edge(1,2,weight=0.5)
G.add_edge(1,3,weight=1)
G.add_edge(1,4,weight=1)
G.add_edge(2,1,weight=1)
G.add_edge(2,4,weight=1)
G.add_edge(3,1,weight=1)
G.add_edge(4,2,weight=1)
G.add_edge(4,3,weight=1)
centrality = nx.pagerank(G,alpha=1)
print centrality

import numpy as np
a = np.array([[0,0.5,1,0],[0.2,0,0,0.5],[0.4,0,0,0.5],[0.4,0.5,0,0]])
b=np.array([[0.25],[0.25],[0.25],[0.25]])
for _ in range(200):
    b = a.dot(b)
