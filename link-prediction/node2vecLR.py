#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 22:55:53 2017

@author: zhangchi
"""

# node2vec + logistic regression

import networkx as nx

# generate input file for node2vec

def generateInputFileForNode2vec():
    G = nx.Graph()
    File = open("USAir.txt","r") # 0.1, 0.2, 0.3这附近比较好
    for line in File:
        lineList = line.strip().split("    ")
        nodeA = int(lineList[0])
        nodeB = int(lineList[1])
        G.add_edge(nodeA,nodeB)
        
    nodeList = G.nodes()
    nodeList.sort()
    for node in nodeList:
        print str(node) + " " + " ".join([str(item) for item in G[node]])

        
# generateInputFileForNode2vec()