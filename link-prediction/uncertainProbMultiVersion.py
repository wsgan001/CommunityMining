#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 22:18:08 2017

@author: zhangchi
"""
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from sklearn.model_selection import train_test_split
from LNBSampleBased import sampleBasedLNBCalculation
import reimplement as ri

def generateDicBySample(G):
    dic = {}
    for node in G:
        dic[node] = [0] # 避免空的之后没法除
    sampleCount = 100
    for _ in sampleCount:
        newG = nx.Graph()
        for nodeA, nodeB in G.edges():
            probability = G[nodeA][nodeB]['prob']
            if np.random.choice([1,0], p=[probability,1-probability]) == 1:
                newG.add_edge(nodeA, nodeB)
        for node in newG:
            dic[node].append(1./len(newG[node]))
    for node in dic:
        dic[node] = sum(dic[node])/sampleCount
    return dic
    

def helper(G, node):
    result = 0
    for item in G[node]:
        result += G[node][item]['prob']
    return result

def common_neighbor(G,mode=0,para=1):
    def predict(u, v):
        result = 0
        for node in nx.common_neighbors(G, u, v):
            if mode == 0:
                #result += (G.edge[node][u]['prob'] ** para) * (G.edge[node][v]['prob'] ** para)
                result += ((G.edge[node][u]['prob'] ** para) * (G.edge[node][v]['prob'] ** para)) / helper(G, node)#len(G[node])
            elif mode == 1:
                #result += (G.edge[node][u]['prob'] ** para) + (G.edge[node][v]['prob'] ** para)
                result += ((G.edge[node][u]['prob'] ** para) * (G.edge[node][v]['prob'] ** para)) / len(G[node])
            else:
                result += 1
        return result
    return ((u, v, predict(u, v)) for u, v in nx.non_edges(G))

def LNBSample(G,para,beyesPara):
    nodeNumber = len(G.nodes())
    M = nodeNumber * (nodeNumber - 1) / 2
    MT = 0
    for a, b in G.edges():
        MT += G.edge[a][b]['prob'] ** beyesPara
    s = float(M)/float(MT) - 1
    dic = {}
    for node in G.nodes():
        dic[node] = sampleBasedLNBCalculation(G,node)
    def predict(u, v):
        result = 0
        for node in nx.common_neighbors(G, u, v):
            #result += (np.log10(s) + np.log10(dic[node])) * (G.edge[node][u]['prob'] ** para) * (G.edge[node][v]['prob'] ** para)
            #result += (np.log10(s) + np.log10(dic[node])) / np.log10(len(G[node]))
            result += (np.log10(s) + np.log10(dic[node])) / len(G[node]) * (G.edge[node][u]['prob'] ** para) * (G.edge[node][v]['prob'] ** para)
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
            #result += (np.log10(s) + np.log10(dic[node])) * (G.edge[node][u]['prob'] ** para) * (G.edge[node][v]['prob'] ** para)
            #result += (np.log10(s) + np.log10(dic[node])) / np.log10(len(G[node]))
            result += (np.log10(s) + np.log10(dic[node])) / len(G[node]) * (G.edge[node][u]['prob'] ** para) * (G.edge[node][v]['prob'] ** para)
        return result
    return ((u, v, predict(u, v)) for u, v in nx.non_edges(G))

def LNBVersion2(G):
    # 已知两个节点相连，那么这两个节点的共同邻居包含w的概率是多少
    PWA1 = {}
    PWA2 = {}
    for node in G.nodes():
        PWA1[node] = 0
        PWA2[node] = 0
        
    existEdgeNumber = 0
    nonexistEdgeNumber = 0
        
    for n1, n2 in G.edges():
        probability = G.edge[n1][n2]['prob']
        
        existEdgeNumber += probability
        nonexistEdgeNumber += (1-probability)
        
        n1Neighbor = set(G[n1].keys())
        n2Neighbor = set(G[n2].keys())
        
        intersection = n1Neighbor.intersection(n2Neighbor)
        for node in intersection:
            PWA1[node] += probability * G.edge[n1][node]['prob'] * G.edge[n2][node]['prob']
            PWA2[node] += (1-probability) * G.edge[n1][node]['prob'] * G.edge[n2][node]['prob']
    
    for n1, n2 in nx.non_edges(G):
        nonexistEdgeNumber += 1
        
        n1Neighbor = set(G[n1].keys())
        n2Neighbor = set(G[n2].keys())
        intersection = n1Neighbor.intersection(n2Neighbor)
        for node in intersection:
            PWA2[node] += G.edge[n1][node]['prob'] * G.edge[n2][node]['prob']
    
    for node in G.nodes():
        PWA1[node] = float(PWA1[node]+1)/float(existEdgeNumber-PWA1[node]+1)
        PWA2[node] = float(PWA2[node]+1)/float(nonexistEdgeNumber-PWA2[node]+1)
    
    def predict(u, v):
        result = 0
        for node in nx.common_neighbors(G, u, v):
            #result += np.log10(PWA1[node]/PWA2[node]) * G.edge[node][u]['prob'] * G.edge[node][v]['prob']
            #result += np.log10(PWA1[node]/PWA2[node]) / np.log10(len(G[node]))
            result += np.log10(PWA1[node]/PWA2[node]) / helper(G, node) * G.edge[node][u]['prob'] * G.edge[node][v]['prob']
        return result
    return ((u, v, predict(u, v)) for u, v in nx.non_edges(G))

def LNBVersion3(G,para,beyesPara):
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
                weight = G.edge[node][neighborList[i]]['prob'] * G.edge[node][neighborList[j]]['prob']
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
            #result += (np.log10(s) + np.log10(dic[node])) * (G.edge[node][u]['prob'] ** para) * (G.edge[node][v]['prob'] ** para)
            #result += (np.log10(s) + np.log10(dic[node])) / np.log10(len(G[node]))
            result += (np.log10(s) + np.log10(dic[node])) / helper(G, node) * (G.edge[node][u]['prob'] ** para) * (G.edge[node][v]['prob'] ** para)
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

def addProbNew(G,originG,prob=0.9,percent=0.15):
    for a,b in G.edges():
        value = 0.5 * np.random.randn() + prob
        while value <= 0 or value > 1:
            value = 0.5 * np.random.randn() + prob
        G.edge[a][b]['prob'] = value
        #G.edge[a][b]['weight'] = 1
    count = 0
    countNumber = percent * len(G.edges())
    nodeList = G.degree().keys()
    edgeNumber = len(G.edges()) * 2
    probabilityList = G.degree().values()
    for i in xrange(len(probabilityList)):
        probabilityList[i] = float(probabilityList[i])/float(edgeNumber)
    while count < countNumber:
        nodeA = np.random.choice(nodeList, p=probabilityList)
        nodeB = np.random.choice(nodeList, p=probabilityList)
        while nodeA == nodeB or nodeB in G[nodeA] or originG.has_edge(nodeA,nodeB):
            nodeB = np.random.choice(nodeList, p=probabilityList)
            
        value = 0.5 * np.random.randn() + (1-prob)
        while value <= 0 or value > 1:
            value = 0.5 * np.random.randn() + (1-prob)
    
        G.add_edge(nodeA,nodeB,prob=value)#,weight=1)
        count += 1
    return G


# =============================================================================
# G = nx.Graph()
# File = open("USAir.txt","r") # 0.1, 0.2, 0.3这附近比较好
# for line in File:
#     lineList = line.strip().split("    ")
#     nodeA = int(lineList[0])
#     nodeB = int(lineList[1])
#     G.add_edge(nodeA,nodeB)
# =============================================================================

G = nx.Graph()
File = open("/Users/zhangchi/Desktop/cs690/CommunityMining/community-detection/TAP_core.txt")
for line in File:
    edgeList = line.strip().split('\t')
    G.add_edge(edgeList[0],edgeList[1],prob=float(edgeList[2]))
    
degree_count = Counter(sorted(nx.degree(G).values()))
keys = degree_count.keys()
keys.sort()
values = [degree_count[item] for item in keys]
plt.plot(keys, values, 'y')
plt.show()

modeList = [0]
paraList = [1]#,0,0.3,0.6]#,0.4,0.5,0.6,0.7,0.8,0.9]
for para in paraList:
    for mode in modeList:
        print "para = " + str(para) + " mode = " + str(mode)
        probList = []
        weightList = []
        accuracyList = []
        accuracyCompareList = []
        accuracyCompare1List = []
        accuracyCompare2List = []
        accuracyCompare3List = []
        testNumber = 40
        for _ in xrange(testNumber):
            edgeTrain, edgeTest = train_test_split(G.edges(), test_size=0.1)
            
            newG = nx.Graph()
            for nodeA, nodeB in edgeTrain:
                #newG.add_edge(nodeA,nodeB)
                newG.add_edge(nodeA,nodeB,prob=G.edge[nodeA][nodeB]['prob'])
            #newG = addProb(newG,prob=0.8,percent=0.2)
            #newG = addProbNew(newG,G,prob=0.8,percent=0.2)
            
            degree_count = Counter(sorted(nx.degree(newG).values()))
            keys = degree_count.keys()
            keys.sort()
            values = [degree_count[item] for item in keys]
            plt.plot(keys, values, 'y')
            plt.show()
            
            # compare
            
            preds = common_neighbor(newG,0)
            
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
            probList.append(float(right)/topK*1.0)
            
            # compare
            
            preds = common_neighbor(newG,1)
            
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
            weightList.append(float(right)/topK*1.0)
            
# =============================================================================
#             # compare
#             
#             #preds = LNB(newG,1,1)
#             preds = LNBSample(newG,para,1)
#             #preds = common_neighbor(newG,mode,para)
#             #preds = nx.adamic_adar_index(newG)
#             #preds = nx.jaccard_coefficient(newG)
#             
#             result = []
#             for u, v, p in preds:
#                 result.append([u,v,p])
#             result.sort(key=lambda x:x[2],reverse=True)
#             right = 0
#             count = 0
#             topK = 100
#             for nodeA, nodeB, score in result[:topK]:
#                 if G.has_edge(nodeA,nodeB):
#                     right += 1
#                     #print str(count) + ": success"
#                 else:
#                     #print str(count) + ": fail"
#                     pass
#                 count += 1
#             print float(right)/topK*1.0
#             accuracyList.append(float(right)/topK*1.0)
# =============================================================================
            
# =============================================================================
#             # compare
#             
#             preds = LNB(newG,para,1)
#             #preds = LNBSample(newG,0,1)
#             #preds = common_neighbor(newG,mode,para)
#             #preds = nx.adamic_adar_index(newG)
#             #preds = nx.jaccard_coefficient(newG)
#             
#             result = []
#             for u, v, p in preds:
#                 result.append([u,v,p])
#             result.sort(key=lambda x:x[2],reverse=True)
#             right = 0
#             count = 0
#             topK = 100
#             for nodeA, nodeB, score in result[:topK]:
#                 if G.has_edge(nodeA,nodeB):
#                     right += 1
#                     #print str(count) + ": success"
#                 else:
#                     #print str(count) + ": fail"
#                     pass
#                 count += 1
#             print float(right)/topK*1.0
#             accuracyCompareList.append(float(right)/topK*1.0)
# =============================================================================
            
            # compare
            
            preds = ri.LNB(newG)
            #preds = LNBSample(newG,0,1)
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
            accuracyCompare1List.append(float(right)/topK*1.0)
            
            # compare
            
            preds = LNBVersion2(newG)
            #preds = LNBSample(newG,0,1)
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
            accuracyCompare2List.append(float(right)/topK*1.0)
            
            # compare
            
            preds = LNBVersion3(newG,para,1)
            #preds = LNBSample(newG,0,1)
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
            accuracyCompare3List.append(float(right)/topK*1.0)
            
            print "-----------"
            
        print probList
        print sum(probList)*1.0/testNumber
        print weightList
        print sum(weightList)*1.0/testNumber
        print accuracyList
# =============================================================================
#         print sum(accuracyList)*1.0/testNumber
#         print accuracyCompareList
# =============================================================================
# =============================================================================
#         print sum(accuracyCompareList)*1.0/testNumber
#         print accuracyCompare1List
# =============================================================================
        print sum(accuracyCompare1List)*1.0/testNumber
        print accuracyCompare2List
        print sum(accuracyCompare2List)*1.0/testNumber
        print accuracyCompare3List
        print sum(accuracyCompare3List)*1.0/testNumber