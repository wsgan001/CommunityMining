#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 10:22:29 2017

@author: zhangchi
"""

import networkx as nx
from ML_Handicapped_Paths import betweenness_centrality
import matplotlib.pyplot as plt
import numpy as np
from closeness import closeness_centrality
#from ML_Paths import betweenness_centrality

def changeWeight(G):
    for nodeA, nodeB in G.edges():
        #if G[nodeA][nodeB]['weight'] <= 0.2:
         #   G[nodeA][nodeB]['weight'] = 1000
        #else:
         #   G[nodeA][nodeB]['weight'] = 1.0 / G[nodeA][nodeB]['weight']
        G[nodeA][nodeB]['newWeight'] = G[nodeA][nodeB]['length'] / (G[nodeA][nodeB]['weight']**0.5)
        #G[nodeA][nodeB]['weight'] = np.tan(np.pi*(1-G[nodeA][nodeB]['weight']))+1
        #G[nodeA][nodeB]['weight'] = 1.0 / np.exp(G[nodeA][nodeB]['weight'])
        #G[nodeA][nodeB]['weight'] = np.exp(-G[nodeA][nodeB]['weight'])
        #G[nodeA][nodeB]['weight'] = 1.0 / G[nodeA][nodeB]['weight'] -np.log( G[nodeA][nodeB]['weight'])
        #G[nodeA][nodeB]['weight'] = -np.log( G[nodeA][nodeB]['weight'])
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
    
def generateProbabilisticGraph():    
    G = nx.random_partition_graph([30,50,80],0.4,0.05)
    for nodeA, nodeB in G.edges():
        G[nodeA][nodeB]['weight'] = -np.random.uniform()+1
        G[nodeA][nodeB]['length'] = np.random.uniform(1,3)
    return G
    
result = []
i = 58
G = generateProbabilisticGraph()

#x = betweenness_centrality(G)
x = closeness_centrality(G)
sorted_x = {key: rank for rank, key in enumerate(sorted(x, key=x.get, reverse=True), 1)}

G = changeWeight(G)
#y = nx.betweenness_centrality(G,weight = 'newWeight')
y = nx.closeness_centrality(G,distance = 'newWeight')
sorted_y = {key: rank for rank, key in enumerate(sorted(y, key=y.get, reverse=True), 1)}

difference = 0
for key in sorted_x:
    plt.scatter(sorted_x[key], sorted_y[key])
    difference = abs(sorted_x[key] - sorted_y[key]) + difference
plt.show()
print difference

result = None
for i in range(100):
    print i
    newG = sampleGraph(G)
    #z = nx.betweenness_centrality(newG,weight='length')
    z = nx.closeness_centrality(newG,distance ='length')
    sorted_z = {key: rank for rank, key in enumerate(sorted(z, key=z.get, reverse=True), 1)}
    #sorted_z = z
    if result is None:
        result = sorted_z
    else:
        for item in result:
            result[item] = result[item] + sorted_z[item]
sorted_z = {key: rank for rank, key in enumerate(sorted(result, key=result.get, reverse=False), 1)}

differenceA = 0
for key in sorted_y:
    if key in sorted_z:
        plt.scatter(sorted_z[key], sorted_y[key])
        differenceA = differenceA + abs(sorted_z[key] - sorted_y[key])
plt.show()
print differenceA

differenceB = 0
for key in sorted_x:
    if key in sorted_z:
        plt.scatter(sorted_z[key], sorted_x[key])
        differenceB = differenceB + abs(sorted_z[key] - sorted_x[key])
plt.show()
print differenceB