#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 13:51:46 2017

@author: zhangchi
"""

import networkx as nx

def findUnvisitedNode(G):
    unvisitedList = []
    for node in G.node:
        if G.node[node]['visit'] == False:
            unvisitedList.append(node)
    return unvisitedList
    
def findPathProbMaxNode(G,unvisitedList):
    maxNode = None
    value = -1
    for node in unvisitedList:
        if G.node[node]['path_probs'] > value:
            value = G.node[node]['path_probs']
            maxNode = node
    return maxNode

def findUnvisitedNeighbors(G,cur):
    neighbors = []
    for node in G.edge[cur]:
        if G.node[node]['visit'] == False:
            neighbors.append(node)
    return neighbors
    
G = nx.Graph()
G.add_edge('a','c',weight=0.95)
G.add_edge('c','d',weight=0.95)
G.add_edge('b','d',weight=0.8)
G.add_edge('a','d',weight=0.8)
G.add_edge('b','c',weight=0.65)
G.add_edge('c','e',weight=0.65)
G.add_edge('d','e',weight=0.8)
G.add_edge('c','f',weight=0.8)
G.add_edge('d','f',weight=0.8)

for node in G.node:
    G.node[node]['visit'] = False
    G.node[node]['path_probs'] = 0
    G.node[node]['previous'] = -1

G.node['a']['path_probs'] = 1

while len(findUnvisitedNode(G)) > 0:
    unvistedNode = findUnvisitedNode(G)
    cur = findPathProbMaxNode(G,unvistedNode)
    neighbors = findUnvisitedNeighbors(G,cur)
    for o in neighbors:
        if G.node[cur]['path_probs'] * G.edge[cur][o]['weight'] > G.node[o]['path_probs']:
            G.node[o]['path_probs'] = G.node[cur]['path_probs'] * G.edge[cur][o]['weight']
            G.node[o]['previous'] = cur
    G.node[cur]['visit'] = True
