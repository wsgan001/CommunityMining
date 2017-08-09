#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 18:25:59 2017

@author: zhangchi
"""

# start link prediction

import networkx as nx
from sklearn.model_selection import train_test_split

G = nx.Graph()
File = open("USAir.txt","r")
for line in File:
    lineList = line.strip().split("    ")
    nodeA = int(lineList[0])
    nodeB = int(lineList[1])
    G.add_edge(nodeA,nodeB)

accuracyList = []
for count in xrange(100):
    print count
    edgeTrain, edgeTest = train_test_split(G.edges(), test_size=0.1)
    
    newG = nx.Graph()
    for nodeA, nodeB in edgeTrain:
        newG.add_edge(nodeA,nodeB)
    preds = nx.adamic_adar_index(newG)
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

