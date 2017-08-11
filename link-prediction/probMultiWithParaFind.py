#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 01:24:23 2017

@author: zhangchi
"""

import networkx as nx
import numpy as np
from sklearn.model_selection import train_test_split

def common_neighbor(G,mode=0,para=1):
    def predict(u, v):
        result = 0
        for node in nx.common_neighbors(G, u, v):
            if mode == 0:
                result += (G.edge[node][u]['prob'] ** para) * (G.edge[node][v]['prob'] ** para)
            elif mode == 1:
                result += (G.edge[node][u]['prob'] ** para) + (G.edge[node][v]['prob'] ** para)
            else:
                result += 1
        return result
    return ((u, v, predict(u, v)) for u, v in nx.non_edges(G))

def LNB(G,para,beyesPara):
    nodeNumber = len(G.nodes())
    M = nodeNumber * (nodeNumber - 1) / 2
    MT = 0
    for a, b in G.edges():
        MT += G.edge[a][b]['prob'] ** beyesPara
    s = float(M)/float(MT) - 1
    dic = {}
    for node in G.nodes():
        neighborList = G[node].keys()
        length = len(neighborList)
        connected = 0
        disconnected = 0
        for i in xrange(length-1):
            for j in xrange(i+1,length):
                weight = 1#G.edge[node][neighborList[i]]['prob'] * G.edge[node][neighborList[j]]['prob']
                if G.has_edge(neighborList[i],neighborList[j]):
                    prob = G.edge[neighborList[i]][neighborList[j]]['prob'] ** beyesPara
                    connected += prob * weight
                    disconnected += (1-prob) * weight
                else:
                    disconnected += 1 * weight
        dic[node] = float(connected+1)/float(disconnected+1)
    def predict(u, v):
        result = 0
        for node in nx.common_neighbors(G, u, v):
            result += (np.log10(s) + np.log10(dic[node])) * (G.edge[node][u]['prob'] ** para) * (G.edge[node][v]['prob'] ** para)
            #result += (np.log10(s) + np.log10(dic[node])) / np.log10(len(G[node]))
            #result += (np.log10(s) + np.log10(dic[node])) / len(G[node])
        return result
    return ((u, v, predict(u, v)) for u, v in nx.non_edges(G))

def addProb(G,prob=0.9,percent=0.15):
    for a,b in G.edges():
        value = 0.5 * np.random.randn() + prob
        while value <= 0 or value > 1:
            value = 0.5 * np.random.randn() + prob
        G.edge[a][b]['prob'] = value
        #G.edge[a][b]['weight'] = 1
    count = 0
    countNumber = percent * len(G.edges())
    nodeList = G.nodes()
    nodeNumber = len(nodeList)
    while count < countNumber:
        nodeA = nodeList[np.random.randint(nodeNumber)]
        nodeB = nodeList[np.random.randint(nodeNumber)]
        while nodeA == nodeB or nodeB in G[nodeA]:
            nodeB = nodeList[np.random.randint(nodeNumber)]
            
        value = 0.5 * np.random.randn() + (1-prob)
        while value <= 0 or value > 1:
            value = 0.5 * np.random.randn() + (1-prob)
    
        G.add_edge(nodeA,nodeB,prob=value)#,weight=1)
        count += 1
    return G

G = nx.Graph()
File = open("USAir.txt","r") # 0.1, 0.2, 0.3这附近比较好
for line in File:
    lineList = line.strip().split("    ")
    nodeA = int(lineList[0])
    nodeB = int(lineList[1])
    G.add_edge(nodeA,nodeB)

# =============================================================================
# G = nx.Graph()
# File = open("/Users/zhangchi/Desktop/cs690/CommunityMining/community-detection/TAP_core.txt")
# for line in File:
#     edgeList = line.strip().split('\t')
#     G.add_edge(edgeList[0],edgeList[1],prob=float(edgeList[2]))
# =============================================================================

modeList = [0]
paraList = [1]#,0.4,0.5,0.6,0.7,0.8,0.9]
for para in paraList:
    for mode in modeList:
        print "para = " + str(para) + " mode = " + str(mode)
        accuracyList = []
        testNumber = 100
        for _ in xrange(testNumber):
            edgeTrain, edgeTest = train_test_split(G.edges(), test_size=0.1)
            
            newG = nx.Graph()
            for nodeA, nodeB in edgeTrain:
                newG.add_edge(nodeA,nodeB)
                #newG.add_edge(nodeA,nodeB,prob=G.edge[nodeA][nodeB]['prob'])
            newG = addProb(newG,prob=0.8,percent=0.2)
            
            preds = LNB(newG,0,0)
            #preds = common_neighbor(newG,mode,para)
            #preds = nx.adamic_adar_index(newG)
            #preds = nx.jaccard_coefficient(newG)
            
            result = []
            for u, v, p in preds:
                result.append([u,v,p])
            result.sort(key=lambda x:x[2],reverse=True)
            right = 0
            count = 0
            topK = 100
            for nodeA, nodeB, score in result[:topK]:
                if G.has_edge(nodeA,nodeB):
                    right += 1
                    #print str(count) + ": success"
                else:
                    #print str(count) + ": fail"
                    pass
                count += 1
            print float(right)/topK*1.0
            accuracyList.append(float(right)/topK*1.0)
            
        print accuracyList
        print sum(accuracyList)*1.0/testNumber