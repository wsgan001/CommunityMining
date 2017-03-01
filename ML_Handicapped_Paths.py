#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 15:53:42 2017

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
    
def findPosteriorProbMaxNode(G,unvisitedList):
    maxNode = None
    value = -1
    for node in unvisitedList:
        if G.node[node]['posterior_probs'] > value:
            value = G.node[node]['posterior_probs']
            maxNode = node
    return maxNode

def findUnvisitedNeighbors(G,cur):
    neighbors = []
    for node in G.edge[cur]:
        if G.node[node]['visit'] == False:
            neighbors.append(node)
    return neighbors

def ML_Handicapped_Paths(G,index):
    for node in G.node:
        G.node[node]['visit'] = False
        G.node[node]['path_probs'] = 0
        G.node[node]['previous'] = -1
        G.node[node]['posterior_probs'] = 0
        G.node[node]['path_length'] = 0
    
    G.node[index]['path_probs'] = 1
    
    while len(findUnvisitedNode(G)) > 0:
        unvistedNode = findUnvisitedNode(G)
        cur = findPosteriorProbMaxNode(G,unvistedNode)
        neighbors = findUnvisitedNeighbors(G,cur)
        for o in neighbors:
            p_prob = G.node[cur]['path_probs'] * G.edge[cur][o]['weight']
            p_length = G.node[cur]['path_length'] + 1
            p_post = p_prob * (0.5 ** p_length)
            if p_post > G.node[o]['posterior_probs']:
                G.node[o]['path_probs'] = p_prob
                G.node[o]['path_length'] = p_length
                G.node[o]['posterior_probs'] = p_post
                G.node[o]['previous'] = cur
        G.node[cur]['visit'] = True
    return G

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
G = ML_Handicapped_Paths(G,'a')