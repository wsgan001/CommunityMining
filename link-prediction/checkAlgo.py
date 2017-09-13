#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 01:53:36 2017

@author: zhangchi
"""

import networkx as nx
import numpy as np

# 证明每个common neighbor可以独立地计算，就算这个common neighbor c和另一个common neighbor d相连
# 在计算c对RA的影响时，也可以先忽略d

#       A
#    -     -
#   0.8    0.7
#   -        -
# c -- 0.4 -- D 
#   -        -
#   0.6    0.5
#    -     -
#       A
# 上下两个等价，即在计算c对RA的影响时，也可以先忽略d
        #       A
        #    -     -
        #   0.8    0.7
        #   -        -
# E -0.4- C            D -0.4- F
        #   -        -
        #   0.6    0.5
        #    -     -
        #       A
# 另一种手算(0.16+0.35/3)*0.4+(0.24+0.175)*0.6

def common_neighbor(G,u,v):
    result = 0
    for node in nx.common_neighbors(G, u, v):
        result += 1. / float(len(G[node]))
    return result

def generateAllPossibility(length):
    candidate = [0] * length
    count = 0
    total = 2 ** length
    while count < total:
        yield candidate # first time using yield
        count += 1
        temp = 1
        index = 0
        while temp == 1 and index < length:
            if candidate[index] == 0:
                candidate[index] = 1
                temp = 0
            else:
                candidate[index] = 0
                temp = 1
                index += 1
                
G = nx.Graph()
G.add_edge("a","c",prob=0.8)
G.add_edge("a","d",prob=0.7)
G.add_edge("b","c",prob=0.6)
G.add_edge("b","d",prob=0.5)
G.add_edge("c","d",prob=0.4)

# 穷尽可能求精确解

edgeList = G.edges()
length = len(edgeList)
value = 0
for possibility in generateAllPossibility(length):
    newG = nx.Graph()
    for node in G.nodes():
        newG.add_node(node)
    probability = 1
    for exist, (u,v) in zip(possibility, edgeList):
        if exist == 1:
            probability *= G.edge[u][v]['prob']
            newG.add_edge(u, v)
        else:
            probability *= (1 - G.edge[u][v]['prob'])
    value += probability * common_neighbor(newG,"a","b")
print value

# sample求近似解

# =============================================================================
# sampleCount = 1000000
# result = []
# for index in xrange(sampleCount):
#     #print index
#     newG = nx.Graph()
#     for node in G.nodes():
#         newG.add_node(node)
#     for nodeA, nodeB in G.edges():
#         probability = G[nodeA][nodeB]['prob']
#         if np.random.choice([1,0], p=[probability,1-probability]) == 1:
#             newG.add_edge(nodeA, nodeB)
#     result.append(common_neighbor(newG,"a","b"))
# print float(sum(result))/float(len(result))
# =============================================================================
