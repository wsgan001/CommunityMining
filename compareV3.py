#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 15:09:10 2017

@author: zhangchi
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 16:47:06 2017

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
        #G[nodeA][nodeB]['weight'] = 1.0 / G[nodeA][nodeB]['weight']
        #G[nodeA][nodeB]['weight'] = np.tan(np.pi*(1-G[nodeA][nodeB]['weight']))+1
        #G[nodeA][nodeB]['weight'] = 1.0 / np.exp(G[nodeA][nodeB]['weight'])
        #G[nodeA][nodeB]['weight'] = 1.0 / (G[nodeA][nodeB]['weight'])
        G[nodeA][nodeB]['newWeight'] = 1.0 / (G[nodeA][nodeB]['weight']**0.4)
        #G[nodeA][nodeB]['weight'] = np.exp(-G[nodeA][nodeB]['weight'])
        #G[nodeA][nodeB]['weight'] = 1.0 / G[nodeA][nodeB]['weight'] -np.log( G[nodeA][nodeB]['weight'])
        #G[nodeA][nodeB]['weight'] = -np.log( G[nodeA][nodeB]['weight'])
    return G
    
def changeWeightlog(G):
    for nodeA, nodeB in G.edges():
        G[nodeA][nodeB]['newWeight'] = -np.log( G[nodeA][nodeB]['weight'])
    return G

def readNet(input_file, now, sep_char=' '): 
    num_lines = 0
    G = nx.Graph()
    for line in open(input_file):
        num_lines += 1
        line = line.rstrip().split(sep_char)
        if line[1] == line[2]:
            pass
        elif int(line[0]) <= now:
            if G.has_edge(line[1], line[2]) is False:            
                G.add_edge(line[1], line[2], time = [int(line[0])])
            else:
                G[line[1]][line[2]]['time'].append(int(line[0]))
        else:
            break
    return G

def getWeight(timeList, now):
    possibility = 1
    for time in timeList:
        if time <= now:
            possibility = possibility * (1 - np.exp((time-now)/2419200.))
        else:
            break
    linkPossibility = 1 - possibility
    return linkPossibility
        
def updateWeight(G, now):
    for nodeA, nodeB in G.edges():
        timeList = G[nodeA][nodeB]['time']
        G[nodeA][nodeB]['weight'] = getWeight(timeList,now)
    return G
    
def sampleGraphOld(G):
    newG = nx.Graph()
    for nodeA, nodeB in G.edges():
        probability = G[nodeA][nodeB]['weight']
        if np.random.choice([1,0], p=[probability,1-probability]) == 1:
            newG.add_edge(nodeA, nodeB)
    return newG
    
def sampleGraph(G):
    newG = nx.Graph()
    for node in G.nodes():
        newG.add_node(node)
    for nodeA, nodeB in G.edges():
        probability = G[nodeA][nodeB]['weight']
        if np.random.choice([1,0], p=[probability,1-probability]) == 1:
            newG.add_edge(nodeA, nodeB)
    return newG

def generateProbabilisticGraphOld(nodeNumber, edgeNumber):
    G = nx.Graph()
    for i in range(nodeNumber):
        G.add_node(i)
    for _ in range(edgeNumber):
        nodeA = np.random.randint(nodeNumber)
        nodeB = np.random.randint(nodeNumber)
        while G.has_edge(nodeA,nodeB):
            nodeA = np.random.randint(nodeNumber)
            nodeB = np.random.randint(nodeNumber)
        G.add_edge(nodeA,nodeB,weight=-np.random.uniform()+1)
    return G

def generateProbabilisticGraph():    
    G = nx.random_partition_graph([30,50,80],0.4,0.05)
    #G = nx.gaussian_random_partition_graph(150,50,2,0.4,0.05)
    for nodeA, nodeB in G.edges():
        G[nodeA][nodeB]['weight'] = -np.random.uniform()+1
    return G
    
result = []
i = 64
G=readNet('resultFullData.txt',927590400+1209600*i)
G = updateWeight(G, 927590400+1209600*i)
#G = generateProbabilisticGraph()

#x = betweenness_centrality(G)
x = closeness_centrality(G)
sorted_x = {key: rank for rank, key in enumerate(sorted(x, key=x.get, reverse=True), 1)}

G = changeWeight(G)
#y = nx.betweenness_centrality(G,weight = 'newWeight')
y = nx.closeness_centrality(G,distance = 'newWeight')
sorted_y = {key: rank for rank, key in enumerate(sorted(y, key=y.get, reverse=True), 1)}
            
G = changeWeightlog(G)
#a = nx.betweenness_centrality(G,weight = 'newWeight')
a = nx.closeness_centrality(G,distance = 'newWeight')
sorted_a = {key: rank for rank, key in enumerate(sorted(a, key=a.get, reverse=True), 1)}
            
difference = 0
for key in sorted_x:
    plt.scatter(sorted_x[key], sorted_y[key],color = 'Red')
    difference = abs(sorted_x[key] - sorted_y[key]) + difference
plt.plot([0,151],[0,151], color ='Green', linewidth=2.5, linestyle="--")
plt.show()
print difference

#G = updateWeight(G, 927590400+1209600*i)
#G = changeWeight(G)
result = None
for i in range(100):
    print i
    newG = sampleGraph(G)
    #z = nx.betweenness_centrality(newG)
    z = nx.closeness_centrality(newG)
    sorted_z = {key: rank for rank, key in enumerate(sorted(z, key=z.get, reverse=True), 1)}
    #sorted_z = z
    if result is None:
        result = sorted_z
    else:
        for item in result:
            result[item] = result[item] + sorted_z[item]
        '''
        for item in result:
            if item in sorted_z:
                result[item] = result[item] + sorted_z[item]
        for item in sorted_z:
            if item not in result:
                result[item] = sorted_z[item]
        '''
sorted_z = {key: rank for rank, key in enumerate(sorted(result, key=result.get, reverse=False), 1)}

differenceA = 0
for key in sorted_y:
    if key in sorted_z:
        plt.scatter(sorted_z[key], sorted_y[key],color = 'Red')
        differenceA = differenceA + abs(sorted_z[key] - sorted_y[key])
plt.plot([0,151],[0,151], color ='Blue', linewidth=3.5, linestyle="--")
#plt.title('Enron Data: Betweenness Centrality')
plt.title('Enron Data: Closeness Centrality')
plt.xlabel('Sample Rankings')
plt.ylabel('1/(probability^r) Rankings')
plt.show()
print differenceA

differenceB = 0
for key in sorted_x:
    if key in sorted_z:
        plt.scatter(sorted_z[key], sorted_x[key],color = 'Red')
        differenceB = differenceB + abs(sorted_z[key] - sorted_x[key])
plt.plot([0,151],[0,151], color ='Blue', linewidth=3.5, linestyle="--")
#plt.title('Enron Data: Betweenness Centrality')
plt.title('Enron Data: Closeness Centrality')
plt.xlabel('Sample Rankings')
plt.ylabel('ML Rankings')
plt.show()
print differenceB

differenceC = 0
for key in sorted_a:
    if key in sorted_z:
        plt.scatter(sorted_z[key], sorted_a[key],color = 'Red')
        differenceC = differenceC + abs(sorted_z[key] - sorted_a[key])
plt.plot([0,151],[0,151], color ='Blue', linewidth=3.5, linestyle="--")
#plt.title('Enron Data: Betweenness Centrality')
plt.title('Enron Data: Closeness Centrality')
plt.xlabel('Sample Rankings')
plt.ylabel('-log(probability) Rankings')
plt.show()
print differenceC

    
'''
G = nx.Graph()
G.add_edge('a','c',weight=0.6)
G.add_edge('c','d',weight=0.8)
G.add_edge('b','d',weight=0.9)
G.add_edge('a','d',weight=0.8)
G.add_edge('b','c',weight=0.4)
G.add_edge('c','e',weight=0.8)
G.add_edge('d','e',weight=0.3)
G.add_edge('c','f',weight=0.8)
G.add_edge('d','f',weight=0.9)
G.add_edge('e','f',weight=0.8)
G.add_edge('e','g',weight=1)
G.add_edge('e','h',weight=0.66)
G.add_edge('f','g',weight=0.2)
G.add_edge('f','h',weight=0.8)
G.add_edge('g','i',weight=0.8)
G.add_edge('h','i',weight=0.9)
G.add_edge('h','j',weight=0.4)
G.add_edge('b','k',weight=0.8)
G.add_edge('k','i',weight=0.9)
'''