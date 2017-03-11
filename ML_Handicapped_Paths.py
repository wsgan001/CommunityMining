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

def ML_Handicapped_Paths(G,index,beta):
    for node in G.node:
        G.node[node]['visit'] = False
        G.node[node]['path_probs'] = 0
        G.node[node]['previous'] = []
        G.node[node]['sigma'] = 0.001
        G.node[node]['posterior_probs'] = 0
        G.node[node]['path_length'] = 0
    
    G.node[index]['path_probs'] = 1
    G.node[index]['posterior_probs'] = 1 #did not show up in paper
    G.node[index]['sigma'] = 1
    S = []
    while len(findUnvisitedNode(G)) > 0:
        unvistedNode = findUnvisitedNode(G)
        cur = findPosteriorProbMaxNode(G,unvistedNode)
        neighbors = findUnvisitedNeighbors(G,cur)
        sigmav = G.node[cur]['sigma']
        S.append(cur)
        for o in neighbors:
            p_prob = G.node[cur]['path_probs'] * G.edge[cur][o]['weight']
            p_length = G.node[cur]['path_length'] + 1
            p_post = p_prob * (beta ** p_length)
            if p_post > G.node[o]['posterior_probs']:
                G.node[o]['path_probs'] = p_prob
                G.node[o]['path_length'] = p_length
                G.node[o]['posterior_probs'] = p_post
                G.node[o]['previous'] = [cur]
                G.node[o]['sigma'] = sigmav
            elif p_post == G.node[o]['posterior_probs']:
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
        G, S = ML_Handicapped_Paths(G,s,0.3)
        #S = G.nodes()
        P = {o:G.node[o]['previous'] for o in G.nodes()}
        sigma = {o:G.node[o]['sigma'] for o in G.nodes()}
        # accumulation
        betweenness = accumulate_basic(betweenness, S, P, sigma, s)
    return betweenness
    
def main():
    G = nx.Graph()
    '''
    G.add_edge('a','c',weight=0.95)
    G.add_edge('c','d',weight=0.95)
    G.add_edge('b','d',weight=0.8)
    G.add_edge('a','d',weight=0.8)
    G.add_edge('b','c',weight=0.65)
    G.add_edge('c','e',weight=0.65)
    G.add_edge('d','e',weight=0.8)
    G.add_edge('c','f',weight=0.8)
    G.add_edge('d','f',weight=0.8)
    
    G, _ = ML_Handicapped_Paths(G,'a',1)
    print G.node
    return G
    '''
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
    
    G, S = ML_Handicapped_Paths(G,'a',1)
    print betweenness_centrality(G)
    return G, S
    '''
    for i in G:
        print i+": " + str(G.node[i]['sigma'])
    print betweenness_centrality(G)
    '''
    
#G, S = main()
    
