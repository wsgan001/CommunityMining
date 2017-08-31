#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 18:21:26 2017

@author: zhangchi
"""

# Link Prediction Based on Local Random Walk

import numpy as np
import networkx as nx

def localRandomWalk(G, t):
    nodeList = G.nodes()
    nodeCount = len(nodeList)
    edgeCount = len(G.edges()) * 2
    nodeDic = {}
    degreeDic = {}
    for index, node in enumerate(nodeList):
        nodeDic[node] = index
        degreeDic[node] = len(G[node])
        
    P = []
    for node in nodeList:
        neighborList = G[node].keys()
        neighborCount = len(neighborList)
        temp = [0] * nodeCount
        for neighbor in neighborList:
            temp[nodeDic[neighbor]] = 1./float(neighborCount)
        P.append(temp)
    P = np.array(P)
    
    Pi = []
    Pi0 = []
    for node in nodeList:
        temp = [0] * nodeCount
        temp[nodeDic[node]] = 1.
        Pi0.append(temp)
    Pi0 = np.array(Pi0)
    Pi.append(Pi0)
        
    for _ in xrange(t):
        Pi.append(np.dot(P,Pi[-1]))
        
    # this two lines only for SRW
    Pi.pop(0)
    Pi.append(sum(Pi))
        
    def predict(u, v):
        return (Pi[-1][nodeDic[u]][nodeDic[v]] * float(degreeDic[u]) + \
                Pi[-1][nodeDic[v]][nodeDic[u]] * float(degreeDic[v])) / float(edgeCount)
        
    return ((u, v, predict(u, v)) for u, v in nx.non_edges(G))

def test():
    G = nx.Graph()
    G.add_edge('a','b')
    G.add_edge('a','c')
    G.add_edge('a','d')
    G.add_edge('b','c')
    G.add_edge('b','d')
    G.add_edge('c','d')
    result = localRandomWalk(G,2)