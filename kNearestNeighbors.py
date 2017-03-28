#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 15:51:50 2017

@author: zhangchi
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

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

G = generateProbabilisticGraph()
G = changeWeight(G)
nodes = G.nodes()[:1]

# Generate Ground Truth
dictionary = {}
t = 10
topKListSampleResult = {}
for node in nodes:
    print node
    dictionary[node] = {}
    for i in range(100):
        newG = sampleGraph(G)
        distanceSample = nx.single_source_dijkstra_path_length(newG,node,weight='length')
        topKListSample = sorted(distanceSample,key=distanceSample.get)[1:t+1]
        for item in topKListSample:
            if item in dictionary[node]:
                dictionary[node][item] += 1
            else:
                dictionary[node][item] = 1
    topKListSampleResult[node] = sorted(dictionary[node],key=dictionary[node].get,reverse=True)[1:t+1]

for k in range(1,31):
    print k
    falsePositiveRateList = []
    truePositiveRateList = []
    for node in nodes:
        print node
        distance = nx.single_source_dijkstra_path_length(G,node,weight='newWeight')
        topKList = sorted(distance,key=distance.get)[1:k+1]
    
        count = 0
        for item in topKListSampleResult[node]:
            if item in topKList:
                count += 1
        falsePositiveRateTemp = (k - count) * 1.0 / (160 - t)
        truePositiveRateTemp = count * 1.0 / t
        falsePositiveRateList.append(falsePositiveRateTemp)
        truePositiveRateList.append(truePositiveRateTemp)
    # ------ #
    falsePositiveRate = np.average(falsePositiveRateList)
    truePositiveRate = np.average(truePositiveRateList)
    print str(falsePositiveRate) + '  '+ str(truePositiveRate)
    plt.scatter(falsePositiveRate, truePositiveRate)

plt.show()
