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

def LNB(G,para,beyesPara=1):
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

def LNBValueGenerator(G):
    nodeNumber = len(G.nodes())
    M = nodeNumber * (nodeNumber - 1) / 2
    MT = 0
    for a, b in G.edges():
        MT += G.edge[a][b]['prob']# ** beyesPara
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
                    prob = G.edge[neighborList[i]][neighborList[j]]['prob']# ** beyesPara
                    connected += prob * weight
                    disconnected += (1-prob) * weight
                else:
                    disconnected += 1 * weight
        dic[node] = float(connected+1)/float(disconnected+1)
    
    candidates = []
    for u, v in nx.non_edges(G):
        result = 0
        for node in nx.common_neighbors(G, u, v):
            result += (np.log10(s) + np.log10(dic[node])) * G.edge[node][u]['prob'] * G.edge[node][v]['prob']
            #result += (np.log10(s) + np.log10(dic[node])) / np.log10(len(G[node]))
            #result += (np.log10(s) + np.log10(dic[node])) / len(G[node])
        candidates.append([u,v,result])
    candidates.sort(key=lambda x:x[2],reverse=True)
    topK = 1000
    commonNeighborDic = {}
    for u, v, _ in candidates[:topK]:
        commonNeighborDic[(u,v)] = []
        for node in nx.common_neighbors(G, u, v):
            commonNeighborDic[(u,v)].append([dic[node],G.edge[node][u]['prob'],G.edge[node][v]['prob']])
    return s, commonNeighborDic

def calculateValueForPara(para,s,dic,TruthG):
    result = []
    for u, v in dic:
        score = 0
        for a, b, c in dic[(u,v)]:
            score += (np.log10(s)+np.log10(a)) * (b**para) * (c**para)
        result.append([u,v,score])
    result.sort(key=lambda x:x[2],reverse=True)
    topK = 100
    right = 0
    for nodeA, nodeB, _ in result[:topK]:
        if TruthG.has_edge(nodeA,nodeB):
            right += 1
    return float(right)/topK*1.0
        
    

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

accuracyTestList = []
accuracyCompare1List = []
accuracyCompare0List = []
testNumber = 20
for _ in xrange(testNumber):
    edgeTrain, edgeTest = train_test_split(G.edges(), test_size=0.1)
    
    newG = nx.Graph()
    for nodeA, nodeB in edgeTrain:
        newG.add_edge(nodeA,nodeB)
        #newG.add_edge(nodeA,nodeB,prob=G.edge[nodeA][nodeB]['prob'])
    newG = addProb(newG,prob=0.8,percent=0.2)
    
    paraTrainNumber = 20
    #ParaGList = []
    sList = []
    commonNeighborDicList = []
    for _ in xrange(paraTrainNumber):
        edgeParaTrain, edgeParaTest = train_test_split(newG.edges(), test_size=0.3)
        ParaG = nx.Graph()
        for nodeA, nodeB in edgeParaTrain:
            ParaG.add_edge(nodeA,nodeB,prob=newG.edge[nodeA][nodeB]['prob'])
        s, commonNeighborDic = LNBValueGenerator(ParaG)
        #ParaGList.append(ParaG)
        sList.append(s)
        commonNeighborDicList.append(commonNeighborDic)
        
    paraList = [-0.1,0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    paraScoreList = []
    for para in paraList:
        scoreList = []
        for i in xrange(paraTrainNumber):
            score = calculateValueForPara(para,sList[i],commonNeighborDicList[i],newG)
            scoreList.append(score)
        paraScoreList.append(float(sum(scoreList))/len(scoreList))
    index = paraScoreList.index(max(paraScoreList))
    para = paraList[index]
    
    print paraScoreList
    print para
    
    # test
    preds = LNB(newG,para)
    
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
    print "test: " + str(float(right)/topK*1.0)
    accuracyTestList.append(float(right)/topK*1.0)
    
    # compare para 1
    preds = LNB(newG,0.2)
    
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
    print "compare 1: " + str(float(right)/topK*1.0)
    accuracyCompare1List.append(float(right)/topK*1.0)
    
    # compare para 0
    preds = LNB(newG,0)
    
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
    print "compare 0: " + str(float(right)/topK*1.0)
    accuracyCompare0List.append(float(right)/topK*1.0)
    
print accuracyTestList
print sum(accuracyTestList)*1.0/testNumber 
print accuracyCompare1List
print sum(accuracyCompare1List)*1.0/testNumber 
print accuracyCompare0List
print sum(accuracyCompare0List)*1.0/testNumber