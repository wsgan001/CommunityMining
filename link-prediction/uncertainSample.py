#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 22:15:03 2017

@author: zhangchi
"""

from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from sklearn.model_selection import train_test_split
from LNBSampleBased import sampleBasedLNBCalculation
import reimplement as ri
from kEdgeProbability import Solution

s = Solution()

def generateDicBySample(G):
    dic = {}
    for node in G:
        dic[node] = [0] # 避免空的之后没法除
    sampleCount = 100
    for index in xrange(sampleCount):
        print index
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

def generateDicBySampleNew(G):
    dic = {}
    for u, v in nx.non_edges(G):
        for node in nx.common_neighbors(G, u, v):
            dic[(node,u,v)] = 0 # 避免空的之后没法除
    return dic
        
    sampleCount = 40
    sampleList = []
    for index in xrange(sampleCount):
        #print index
        newG = nx.Graph()
        for nodeA, nodeB in G.edges():
            probability = G[nodeA][nodeB]['prob']
            if np.random.choice([1,0], p=[probability,1-probability]) == 1:
                newG.add_edge(nodeA, nodeB)
        sampleList.append(newG)
        
    for index,sample in enumerate(sampleList):
        #print index
        for u, v in nx.non_edges(G):
            for node in nx.common_neighbors(G, u, v):
                if sample.has_edge(node,u) and sample.has_edge(node,v):
                    dic[(node,u,v)] += 1./len(sample[node])
            
    for u, v in nx.non_edges(G):
        for node in nx.common_neighbors(G, u, v):
            dic[(node,u,v)] = dic[(node,u,v)]/sampleCount
        
    return dic

def sample(G,node,u,v):
    probList = []
    for item in G[node]:
        if item != u and item != v:
            probList.append(G[node][item]['prob'])
    sampleCount = 20
    result = []
    for _ in xrange(sampleCount):
        count = 2
        for prob in probList:
            if np.random.choice([1,0], p=[prob,1-prob]) == 1:
                count += 1
        result.append(1./count)
    return sum(result)/sampleCount
    

def helper(G, node):
    result = 0
    for item in G[node]:
        result += G[node][item]['prob']
    return result

def common_neighbor(G,dic,mode=0,para=1):
    # 3, 1, 0, 2
    def predict(u, v):
        result = 0
        for node in nx.common_neighbors(G, u, v):
            if mode == -1:
                result += 1.
            elif mode == 2:# weight的做法
                result += G.edge[node][u]['prob'] + G.edge[node][v]['prob']
            elif mode == 4:# 我认为的正确做法
                result += G.edge[node][u]['prob'] * G.edge[node][v]['prob']
            else:
                result += 1.
        return result
    return ((u, v, predict(u, v)) for u, v in nx.non_edges(G))

def common_neighbor_v1(G,dic,mode=0,para=1):
    # 3, 1, 0, 2
    def predict(u, v):
        result = 0
        for node in nx.common_neighbors(G, u, v):
            if mode == 0: #错误做法的修订版（仍然有问题）
                result += ((G.edge[node][u]['prob'] ** para) * (G.edge[node][v]['prob'] ** para)) / helper(G, node)
            elif mode == -1:
                result += 1. / len(G[node])
            elif mode == 1:# 我最开始的错误做法
                result += ((G.edge[node][u]['prob'] ** para) * (G.edge[node][v]['prob'] ** para)) / len(G[node])
            elif mode == 2:# weight的做法
                result += ((G.edge[node][u]['prob'] ** para) + (G.edge[node][v]['prob'] ** para)) / helper(G, node)
            elif mode == 3:# 我认为的正确做法
                result += dic[(node,u,v)]#((G.edge[node][u]['prob'] ** para) * (G.edge[node][v]['prob'] ** para)) * sample(G,node,u,v)
            elif mode == 4:# 我认为的正确做法
                result += s.getScore(dic[node],[G.edge[node][u]['prob'], G.edge[node][v]['prob']])
# =============================================================================
#                 print "---"
#                 probList = []
#                 for neighbor in G[node]:
#                     probList.append(G[node][neighbor]['prob'])
#                 print probList
#                 print dic[node]
#                 print [G.edge[node][u]['prob'], G.edge[node][v]['prob']]
#                 print s.getScore(dic[node],[G.edge[node][u]['prob'], G.edge[node][v]['prob']])
#                 print ((G.edge[node][u]['prob'] ** para) * (G.edge[node][v]['prob'] ** para)) / helper(G, node)
# =============================================================================
# =============================================================================
#                 probList = []
#                 for item in G[node]:
#                     if item != u and item != v:
#                         probList.append(G[node][item]['prob'])
#                 #print probList
#                 result += s.getScoreV2(probList,[G.edge[node][u]['prob'], G.edge[node][v]['prob']])
# =============================================================================
# =============================================================================
#                 # 看看这个近似有没有问题
#                 value1 = s.getScore(dic[node],[G.edge[node][u]['prob'], G.edge[node][v]['prob']])
#                 result += value1
#                 probList = []
#                 for item in G[node]:
#                     if item != u and item != v:
#                         probList.append(G[node][item]['prob'])
#                 #print probList
#                 value2 = s.getScoreV2(probList,[G.edge[node][u]['prob'], G.edge[node][v]['prob']])
#                 if abs(value1-value2) > 0.001 and (value1 > 0.5 or value2 > 0.5):
#                     print value1
#                     print value2
#                     print probList
#                     print [G.edge[node][u]['prob'], G.edge[node][v]['prob']]
#                     print "-----"
# =============================================================================
                
            else:
                result += 1
        return result
    return ((u, v, predict(u, v)) for u, v in nx.non_edges(G))

def LNBVersion2(G):#version2和version3类似，就用version3好了
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
        PWA2[node] = float(PWA2[node]+1)/float(nonexistEdgeNumber-PWA2[node]+1  )
    
    def predict(u, v):
        result = 0
        for node in nx.common_neighbors(G, u, v):
            #result += np.log10(PWA1[node]/PWA2[node]) * G.edge[node][u]['prob'] * G.edge[node][v]['prob']
            #result += np.log10(PWA1[node]/PWA2[node]) / np.log10(len(G[node]))
            result += np.log10(PWA1[node]/PWA2[node]) / helper(G, node) * G.edge[node][u]['prob'] * G.edge[node][v]['prob']
        return result
    return ((u, v, predict(u, v)) for u, v in nx.non_edges(G))

def LNBVersion3(G,dic_input,mode,para,beyesPara):
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
            if mode == 0:#错误做法的修订版（仍然有问题）
                result += (np.log10(s) + np.log10(dic[node])) / helper(G, node) * (G.edge[node][u]['prob'] ** para) * (G.edge[node][v]['prob'] ** para)
            elif mode == 1:# 我最开始的错误做法
                result += (np.log10(s) + np.log10(dic[node])) / len(G[node]) * (G.edge[node][u]['prob'] ** para) * (G.edge[node][v]['prob'] ** para)
            elif mode == 2:# 我认为的正确做法
                result += (np.log10(s) + np.log10(dic[node])) * dic_input[(node,u,v)]
                #result += (np.log10(s) + np.log10(dic[node])) * sample(G,node,u,v) * (G.edge[node][u]['prob'] ** para) * (G.edge[node][v]['prob'] ** para)
            #result += (np.log10(s) + np.log10(dic[node])) * (G.edge[node][u]['prob'] ** para) * (G.edge[node][v]['prob'] ** para)
            #result += (np.log10(s) + np.log10(dic[node])) / np.log10(len(G[node]))
            #result += (np.log10(s) + np.log10(dic[node])) / helper(G, node) * (G.edge[node][u]['prob'] ** para) * (G.edge[node][v]['prob'] ** para)
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
        accuracyCompareList = []
        accuracyCompare0List = []
        accuracyCompare1List = []
        accuracyCompare2List = []
        accuracyCompare3List = []
        accuracyCompare4List = []
        accuracyCompare5List = []
        accuracyCompare6List = []
        accuracyCompare7List = []
        testNumber = 40
        for _ in xrange(testNumber):
            edgeTrain, edgeTest = train_test_split(G.edges(), test_size=0.1)
            
            newG = nx.Graph()
            for nodeA, nodeB in edgeTrain:
                #newG.add_edge(nodeA,nodeB)
                #newG.add_edge(nodeA,nodeB,prob=1)
                newG.add_edge(nodeA,nodeB,prob=G.edge[nodeA][nodeB]['prob'])
            #newG = addProb(newG,prob=0.8,percent=0.2)
            #newG = addProbNew(newG,G,prob=0.8,percent=0.2)
            
# =============================================================================
#             print "start sample"
#             dic = generateDicBySampleNew(newG)
#             print "finish sample"
# =============================================================================
            print "start calculation"
            dic = {}
            for node in newG.nodes():
                probList = []
                for neighbor in newG[node]:
                    probList.append(newG[node][neighbor]['prob'])
                if len(probList) >= 2:
                    dic[node] = s.getDic(probList)
            print "finish calculation"
            
            
            degree_count = Counter(sorted(nx.degree(newG).values()))
            keys = degree_count.keys()
            keys.sort()
            values = [degree_count[item] for item in keys]
            plt.plot(keys, values, 'y')
            plt.show()
            
            # compare
            
            preds = common_neighbor(newG,dic,4)
            
            result = []
            for u, v, p in preds:
                result.append([u,v,p])
            result.sort(key=lambda x:x[2],reverse=True)
            print result[:100]
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
            accuracyCompareList.append(float(right)/topK*1.0)
            
# =============================================================================
#             # compare
#             
#             preds = common_neighbor(newG,dic,3)
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
#             accuracyCompare0List.append(float(right)/topK*1.0)
# =============================================================================
            
            # compare
            
            preds = common_neighbor(newG,dic,1)
            
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
            
            preds = common_neighbor(newG,dic,0)
            #preds = LNB(newG,1,1)
            #preds = LNBSample(newG,para,1)
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
            
            preds = common_neighbor(newG,dic,2)
            #preds = LNB(newG,para,1)
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
            
            
            preds = common_neighbor(newG,dic,-1)
            #preds = LNB(newG,para,1)
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
            accuracyCompare4List.append(float(right)/topK*1.0)
            
# =============================================================================
#             # compare
#             
#             preds = ri.LNB(newG)
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
#             accuracyCompare4List.append(float(right)/topK*1.0)
#             
#             # compare
#             preds = LNBVersion3(newG,dic,0,para,1)
#             #preds = LNBVersion2(newG)
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
#             accuracyCompare5List.append(float(right)/topK*1.0)
#             
#             # compare
#             
#             preds = LNBVersion3(newG,dic,1,para,1)
#             #preds = LNBVersion3(newG,para,1)
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
#             accuracyCompare6List.append(float(right)/topK*1.0)
# =============================================================================
            
# =============================================================================
#             # compare
#             
#             preds = LNBVersion3(newG,dic,2,para,1)
#             #preds = LNBVersion3(newG,para,1)
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
#             accuracyCompare7List.append(float(right)/topK*1.0)
# =============================================================================
            
            print "-----------"
            
        print accuracyCompareList
        print sum(accuracyCompareList)*1.0/testNumber
        print accuracyCompare0List
        print sum(accuracyCompare0List)*1.0/testNumber
        print accuracyCompare1List
        print sum(accuracyCompare1List)*1.0/testNumber
        print accuracyCompare2List
        print sum(accuracyCompare2List)*1.0/testNumber
        print accuracyCompare3List
        print sum(accuracyCompare3List)*1.0/testNumber
        print accuracyCompare4List
        print sum(accuracyCompare4List)*1.0/testNumber
        print accuracyCompare5List
        print sum(accuracyCompare5List)*1.0/testNumber
        print accuracyCompare6List
        print sum(accuracyCompare6List)*1.0/testNumber
        print accuracyCompare7List
        print sum(accuracyCompare7List)*1.0/testNumber