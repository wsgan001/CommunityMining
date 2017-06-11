#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 23:19:22 2017

@author: zhangchi
"""

# start community detection project
# paper reimplementation

import networkx as nx

def generateGraph():
    G = nx.random_partition_graph([30,50],0.2,0.02)
    return G

G = nx.Graph()
G.add_edge(1,2)
G.add_edge(1,3)
G.add_edge(2,3)
G.add_edge(2,4)
G.add_edge(3,4)
G.add_edge(4,5)
G.add_edge(4,6)
D = set([1,2,4])
B = {1:1,2:1,4:3}
S = set([3,5,6])
label = True
R = 0
while label:
    RPrime = -float('inf')
    for node in S:
        tempSet = set(G[node].keys())
        deltaIn = len(tempSet.intersection(D))
        deltaTotal = len(tempSet) - deltaIn
        tempB = dict(B)
        removeSet = set()
        tempLabel = True
        for item in tempSet:
            if item in tempB:
                tempB[item] -= 1
                if tempB[item] == 0:
                    removeSet.add(item)
            else:
                tempLabel = False
        if tempLabel:
            removeSet.add(node)
        count = 0
        for item in removeSet:
            count += len(set(G[item].keys()).intersection(removeSet))
        deltaPrime = count // 2
    
#==============================================================================
# def localCommunityIdentification(G,startNode):
#     D = Set([startNode])
#     B = {startNode:len(G[startNode])}
#     S = Set(G[startNode].keys())
#     label = True
#     R = 0
#     while label:
#         RPrime = -float('inf')
#         for node in S:
#             tempSet = Set(G[node].keys())
#             deltaIn = len(tempSet.intersection(D))
#             deltaTotal = len(tempSet) - deltaIn
#             tempB = dict(B)
#             removeSet = Set()
#             tempLabel = True
#             for item in tempSet:
#                 if item in tempB:
#                     tempB[item] -= 1
#                     if tempB[item] == 0:
#                         removeSet.add(item)
#                 else:
#                     tempLabel = False
#             if tempLabel:
#                 removeSet.add(node)
#             count = 0
#             for item in removeSet:
#                 count += len(Set(G[item].keys()).intersection(removeSet))
#             deltaPrime = count // 2
#==============================================================================
            
            
    
#==============================================================================
# def localCommunityIdentification(G,startNode):
#     D = Set([startNode])
#     B = Set([startNode])
#     S = Set(G[startNode].keys())
#     label = True
#     R = 0
#     while label:
#         RPrime = -float('inf')
#         for node in S:
#             tempSet = Set(G[node].keys())
#             deltaIn = len(tempSet.intersection(D))
#             deltaTotal = len(tempSet) - deltaIn
#             deltaPrime = len(tempSet.intersection(B))
#==============================================================================
        
    