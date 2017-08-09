#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 22:18:08 2017

@author: zhangchi
"""

import networkx as nx
import numpy as np
from sklearn.model_selection import train_test_split

def common_neighbor(G):
    def predict(u, v):
        result = 0
        for node in nx.common_neighbors(G, u, v):
            result += G.edge[node][u]['prob'] * G.edge[node][v]['prob']
        return result
    return ((u, v, predict(u, v)) for u, v in nx.non_edges(G))

def addProb(G,prob=0.9,percent=0.15):
    for a,b in G.edges():
        value = 0.5 * np.random.randn() + prob
        while value <= 0 or value > 1:
            value = 0.5 * np.random.randn() + prob
        G.edge[a][b]['prob'] = value
        #G.edge[a][b]['weight'] = 1
    count = 0
    countNumber = percent * len(G.edges())
    nodeList = G.nodes()
    nodeNumber = len(nodeList)
    while count < countNumber:
        nodeA = nodeList[np.random.randint(nodeNumber)]
        nodeB = nodeList[np.random.randint(nodeNumber)]
        while nodeA == nodeB or nodeB in G[nodeA]:
            nodeB = nodeList[np.random.randint(nodeNumber)]
            
        value = 0.5 * np.random.randn() + (1-prob)
        while value <= 0 or value > 1:
            value = 0.5 * np.random.randn() + (1-prob)
    
        G.add_edge(nodeA,nodeB,prob=value)#,weight=1)
        count += 1
    return G

# =============================================================================
# G = nx.Graph()
# File = open("USAir.txt","r")
# for line in File:
#     lineList = line.strip().split("    ")
#     nodeA = int(lineList[0])
#     nodeB = int(lineList[1])
#     G.add_edge(nodeA,nodeB)
# =============================================================================

G = nx.Graph()
File = open("/Users/zhangchi/Desktop/cs690/CommunityMining/community-detection/TAP_core.txt")
for line in File:
    edgeList = line.strip().split('\t')
    G.add_edge(edgeList[0],edgeList[1],prob=float(edgeList[2]))

accuracyList = []
for count in xrange(10):
    print count
    edgeTrain, edgeTest = train_test_split(G.edges(), test_size=0.1)
    
    newG = nx.Graph()
    for nodeA, nodeB in edgeTrain:
        #newG.add_edge(nodeA,nodeB)
        newG.add_edge(nodeA,nodeB,prob=G.edge[nodeA][nodeB]['prob'])
    #newG = addProb(newG,prob=0.8,percent=0.4)
    
    preds = common_neighbor(newG)
    #preds = nx.adamic_adar_index(newG)
    #preds = nx.jaccard_coefficient(newG)
    
    result = []
    for u, v, p in preds:
        result.append([u,v,p])
    result.sort(key=lambda x:x[2],reverse=True)
    right = 0
    for nodeA, nodeB, score in result[:100]:
        if G.has_edge(nodeA,nodeB):
            right += 1
    accuracyList.append(float(right)/100.)
    
print sum(accuracyList)/10.