#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 15:51:50 2017

@author: zhangchi
"""

import networkx as nx
import numpy as np

def generateProbabilisticGraph():    
    G = nx.random_partition_graph([30,50,80],0.4,0.05)
    for nodeA, nodeB in G.edges():
        G[nodeA][nodeB]['weight'] = -np.random.uniform() + 1
        G[nodeA][nodeB]['length'] = np.random.uniform(1,3)
    return G
    
def changeWeight(G):
    for nodeA, nodeB in G.edges():
        G[nodeA][nodeB]['newWeight'] = G[nodeA][nodeB]['length'] / (G[nodeA][nodeB]['weight']**0.4)
    return G

def sampleGraph(G):
    newG = nx.Graph()
    for node in G.nodes():
        newG.add_node(node)
    for nodeA, nodeB in G.edges():
        probability = G[nodeA][nodeB]['weight']
        lengthValue = G[nodeA][nodeB]['length']
        if np.random.choice([1,0], p=[probability,1-probability]) == 1:
            newG.add_edge(nodeA, nodeB,length=lengthValue)
    return newG
    
k = 10
G = generateProbabilisticGraph()
G = changeWeight(G)
distance = nx.single_source_dijkstra_path_length(G,1,weight='newWeight')
topKList = sorted(distance,key=distance.get)[1:k+1]

dictionary = {}
for i in range(100):
    newG = sampleGraph(G)
    distanceSample = nx.single_source_dijkstra_path_length(newG,1,weight='length')
    topKListSample = sorted(distanceSample,key=distanceSample.get)[1:k+1]
    for item in topKListSample:
        if item in dictionary:
            dictionary[item] += 1
        else:
            dictionary[item] = 1


