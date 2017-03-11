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

def ML_Paths(G,index):
    for node in G.node:
        G.node[node]['visit'] = False
        G.node[node]['path_probs'] = 0
        G.node[node]['previous'] = []
        G.node[node]['sigma'] = 0.001
    
    G.node[index]['path_probs'] = 1
    G.node[index]['sigma'] = 1
    S = []
    while len(findUnvisitedNode(G)) > 0:
        unvistedNode = findUnvisitedNode(G)
        cur = findPathProbMaxNode(G,unvistedNode)
        neighbors = findUnvisitedNeighbors(G,cur)
        sigmav = G.node[cur]['sigma']
        S.append(cur)
        for o in neighbors:
            if G.node[cur]['path_probs'] * G.edge[cur][o]['weight'] > G.node[o]['path_probs']:
                G.node[o]['path_probs'] = G.node[cur]['path_probs'] * G.edge[cur][o]['weight']
                G.node[o]['previous'] = [cur]
                G.node[o]['sigma'] = sigmav
            elif G.node[cur]['path_probs'] * G.edge[cur][o]['weight'] == G.node[o]['path_probs']:
                G.node[o]['previous'].append(cur)
                G.node[o]['sigma'] += sigmav
        G.node[cur]['visit'] = True
    return G, S
    
def accumulate_basic(betweenness, S, P, sigma, s):
    delta = dict.fromkeys(S, 0)
    while S:
        w = S.pop()
        coeff = (1.0 + delta[w]) / sigma[w]
        for v in P[w]: # the order of item in P[w] doesn't matter
            delta[v] += sigma[v] * coeff
        if w != s:
            betweenness[w] += delta[w]
    return betweenness

def betweenness_centrality(G):
    betweenness = dict.fromkeys(G, 0.0)  # b[v]=0 for v in G
    for s in G:
        G, S = ML_Paths(G,s)
        #S = G.nodes()
        P = {o:G.node[o]['previous'] for o in G.nodes()}
        sigma = {o:G.node[o]['sigma'] for o in G.nodes()}
        # accumulation
        betweenness = accumulate_basic(betweenness, S, P, sigma, s)
    return betweenness

def main():    
    G = nx.Graph()
    G.add_edge('a','c',weight=0.8)
    G.add_edge('c','d',weight=0.8)
    G.add_edge('b','d',weight=0.8)
    G.add_edge('a','d',weight=0.8)
    G.add_edge('b','c',weight=0.8)
    G.add_edge('c','e',weight=0.8)
    G.add_edge('d','e',weight=0.8)
    G.add_edge('c','f',weight=0.8)
    G.add_edge('d','f',weight=0.8)
    G.add_edge('e','f',weight=0.8)
    G.add_edge('e','g',weight=0.8)
    G.add_edge('e','h',weight=0.8)
    G.add_edge('f','g',weight=0.8)
    G.add_edge('f','h',weight=0.8)
    G.add_edge('g','i',weight=0.8)
    G.add_edge('h','i',weight=0.8)
    G.add_edge('h','j',weight=0.8)
    G.add_edge('b','k',weight=0.8)
    G.add_edge('k','i',weight=0.8)
    
    G, S = ML_Paths(G,'a')
    for i in G:
        print i+": " + str(G.node[i]['sigma'])
    print betweenness_centrality(G)

'''
betweenness = dict.fromkeys(G, 0.0)
G, S = ML_Paths(G,'a')
#S = G.nodes() # Wrong
P = {o:G.node[o]['previous'] for o in G.nodes()}
sigma = {o:(G.node[o]['sigma']) for o in G.nodes()}
# accumulation
betweenness = accumulate_basic(betweenness, S, P, sigma, 'a')
'''