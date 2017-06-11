#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 23:19:22 2017

@author: zhangchi
"""

# start community detection project
# paper reimplementation

import networkx as nx
from sets import Set

def generateGraph():
    G = nx.random_partition_graph([30,50],0.2,0.02)
    return G
    
def localCommunityIdentification(G,startNode):
    D = Set([startNode])
    B = Set([startNode])
    S = Set(G[startNode].keys())
    label = True
    R = 0
    while label:
        RPrime = -float('inf')
        for node in S:
            tempSet = Set(G[node].keys())
            deltaIn = len(tempSet.intersection(D))
            deltaTotal = len(tempSet) - deltaIn
            deltaPrime = len(tempSet.intersection(B))
        
    