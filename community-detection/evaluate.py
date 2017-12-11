#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 00:20:28 2017

@author: zhangchi
"""

import networkx as nx
import numpy as np
import myUncertain_v1 as mU1

def calculateUncertainR(G, D):
    def helperA(node, nodeSet):
        count = 0
        for item in nodeSet:
            if item in G.edge[node]:
                count += G.edge[node][item]['prob']
        return count
    O = set(G.nodes()).difference(D)
    C = set()
    B = set()
    for item in D:
        if len(set(G[item].keys()).intersection(O)) > 0:
            B.add(item)
        else:
            C.add(item)
    if len(B) == 0:
        return 1
    else:
        countIn = 0
        countBorder = 0
        countOut = 0
        for item in B:
            #temp = set(G[item].keys())
            countIn += helperA(item,C)#len(temp.intersection(C))
            countBorder += helperA(item,B)#len(temp.intersection(B))
            countOut += helperA(item,O)#len(temp.intersection(O))
        BIn = countIn + float(countBorder) / 2.
        BTotal = countOut + BIn
        return float(BIn) / float(BTotal)

def calculateR(G, D):
    O = set(G.nodes()).difference(D)
    C = set()
    B = set()
    for item in D:
        if len(set(G[item].keys()).intersection(O)) > 0:
            B.add(item)
        else:
            C.add(item)
    if len(B) == 0:
        return 1
    else:
        countIn = 0
        countBorder = 0
        countOut = 0
        for item in B:
            temp = set(G[item].keys())
            countIn += len(temp.intersection(C))
            countBorder += len(temp.intersection(B))
            countOut += len(temp.intersection(O))
        BIn = countIn + float(countBorder) / 2.
        BTotal = countOut + BIn
        return float(BIn) / float(BTotal)
        
def sampleGraph(G, sampleNumber):
    GraphList = []
    for _ in xrange(sampleNumber):
        newG = nx.Graph()
        for node in G.nodes():
            newG.add_node(node)
        for nodeA, nodeB in G.edges():
            probability = G[nodeA][nodeB]['prob']
            if np.random.choice([1,0], p=[probability,1-probability]) == 1:
                newG.add_edge(nodeA, nodeB)
        GraphList.append(newG)
    return GraphList

#==============================================================================
# G = nx.Graph()
# File = open("binary_networks/network.dat","r")
# for line in File:
#     nodeA, nodeB = line.strip().split("\t")
#     G.add_edge(int(nodeA),int(nodeB))
# dic = {}
# label = {}
# File = open("binary_networks/community.dat","r")
# for line in File:
#     node, community = line.strip().split("\t")
#     label[int(node)] = int(community)
#     if int(community) not in dic:
#         dic[int(community)] = set([int(node)])
#     else:
#         dic[int(community)].add(int(node))
# print calculateR(G,set([186, 230, 6, 743, 487, 54]))
#==============================================================================
        
def main():
    G = nx.Graph()
    G.add_edge(1,2)
    G.add_edge(1,3)
    G.add_edge(1,4)
    G.add_edge(2,3)
    G.add_edge(2,4)
    G.add_edge(2,13)
    G.add_edge(3,4)
    G.add_edge(3,7)
    G.add_edge(3,13)
    G.add_edge(4,9)
    G.add_edge(4,13)
    G.add_edge(5,6)
    G.add_edge(5,7)
    G.add_edge(5,8)
    G.add_edge(5,13)
    G.add_edge(6,7)
    G.add_edge(6,8)
    G.add_edge(6,10)
    G.add_edge(6,13)
    G.add_edge(7,8)
    G.add_edge(7,13)
    G.add_edge(9,10)
    G.add_edge(9,11)
    G.add_edge(9,12)
    G.add_edge(10,11)
    G.add_edge(10,12)
    G.add_edge(11,12)
    G.add_edge(11,13)
    D = set([1,2,3,4,13])
    print calculateR(G,D)
    
def uncertainMain():
    G = nx.Graph()
    G.add_edge(1,2,prob=0.9)
    G.add_edge(1,3,prob=0.9)
    G.add_edge(1,4,prob=0.9)
    G.add_edge(1,5,prob=0.9)
    G.add_edge(1,6,prob=0.9)
    G.add_edge(2,3,prob=0.9)
    G.add_edge(2,4,prob=0.9)
    G.add_edge(2,5,prob=0.9)
    G.add_edge(2,6,prob=0.9)
    G.add_edge(3,4,prob=0.9)
    G.add_edge(3,5,prob=0.9)
    G.add_edge(3,6,prob=0.9)
    G.add_edge(4,5,prob=0.9)
    G.add_edge(4,6,prob=0.9)
    G.add_edge(5,6,prob=0.9)
    
    G.add_edge(6,7,prob=0.8)
    
    G.add_edge(7,8,prob=0.8)
    G.add_edge(7,9,prob=0.8)
    G.add_edge(7,10,prob=0.8)
    G.add_edge(8,9,prob=0.8)
    G.add_edge(8,10,prob=0.8)
    G.add_edge(9,10,prob=0.8)
    #G.add_edge(9,11,prob=0.8)
    start = 6
    for start in G.nodes():
        result,R = mU1.localCommunityIdentification(G,start,0,False)
        Rcheck = calculateUncertainR(G, result)
        if R != Rcheck:
            print R
            print Rcheck
            print "fuuuuuck!"
        else:
            print R
            print "hoho"
            
#uncertainMain()