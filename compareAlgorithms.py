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
#from ML_Paths import betweenness_centrality

def changeWeight(G):
    for nodeA, nodeB in G.edges():
        G[nodeA][nodeB]['weight'] = 1.0 / G[nodeA][nodeB]['weight']
        #G[nodeA][nodeB]['weight'] = -np.log( G[nodeA][nodeB]['weight'])
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

def findRank(sorted_x, number):
    length = len(sorted_x)
    count = 0
    for item in sorted_x:
        count = count + 1
        if item[0] == number:
            #return length-count
            return int(151.*(length-count)/length)
    #return length
    return 151

result = []
i = 67
G=readNet('resultFullData.txt',927590400+1209600*i)
#nx.draw(G)
G = updateWeight(G, 927590400+1209600*i)

x = betweenness_centrality(G)
sorted_x = {key: rank for rank, key in enumerate(sorted(x, key=x.get, reverse=True), 1)}
G = changeWeight(G)
y = nx.betweenness_centrality(G,weight = 'weight')
sorted_y = {key: rank for rank, key in enumerate(sorted(y, key=y.get, reverse=True), 1)}
difference = 0
for key in sorted_x:
    plt.scatter(sorted_x[key], sorted_y[key])
    difference = abs(sorted_x[key] - sorted_y[key]) + difference
plt.show()
print difference

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