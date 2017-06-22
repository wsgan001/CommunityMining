#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 00:20:28 2017

@author: zhangchi
"""

import networkx as nx

def calculateR(G, D):
    O = set(G.nodes()).difference(D)
    C = set()
    B = set()
    for item in D:
        if len(set(G[item].keys()).intersection(O)) > 0:
            B.add(item)
        else:
            C.add(item)
    if len(B) == 0:
        return 1
    else:
        countIn = 0
        countBorder = 0
        countOut = 0
        for item in B:
            temp = set(G[item].keys())
            countIn += len(temp.intersection(C))
            countBorder += len(temp.intersection(B))
            countOut += len(temp.intersection(O))
        BIn = countIn + float(countBorder) / 2.
        BTotal = countOut + BIn
        return float(BIn) / float(BTotal)
        
G = nx.Graph()
G.add_edge(1,2)
G.add_edge(1,3)
G.add_edge(1,4)
G.add_edge(2,3)
G.add_edge(2,4)
G.add_edge(2,13)
G.add_edge(3,4)
G.add_edge(3,7)
G.add_edge(3,13)
G.add_edge(4,9)
G.add_edge(4,13)
G.add_edge(5,6)
G.add_edge(5,7)
G.add_edge(5,8)
G.add_edge(5,13)
G.add_edge(6,7)
G.add_edge(6,8)
G.add_edge(6,10)
G.add_edge(6,13)
G.add_edge(7,8)
G.add_edge(7,13)
G.add_edge(9,10)
G.add_edge(9,11)
G.add_edge(9,12)
G.add_edge(10,11)
G.add_edge(10,12)
G.add_edge(11,12)
G.add_edge(11,13)
D = set([1,2,3,4,13])
print calculateR(G,D)
    