#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 16:11:20 2017

@author: zhangchi
"""

# local community detection with uncertainty

import networkx as nx
import numpy as np
import random
from evaluate import calculateR
import evaluate
import uncertainAlgorithm_v1 as uav1
import os, sys

sys.path.append(os.getcwd()+'/python_mcl-master/mcl/')
from mcl_clustering import mcl

class Save(object):
    def __init__(self, label, RPrime, popNode, shareSNodeCount):
        self.label = label
        self.RPrime = RPrime
        self.popNode = popNode
        self.shareSNodeCount = shareSNodeCount
        self.tempB = None
        self.tempBIn = None
        self.tempBTotal = None
        self.removeSet = None       

class SampleGraph(object):
    def __init__(self, G, D, B, S, previousRemove, R, BIn, BTotal):
        self.G = G
        self.D = D
        self.B = B
        self.S = S
        self.previousRemove = previousRemove
        self.R = R
        self.BIn = BIn
        self.BTotal = BTotal

def main2():
    # data 4
    #uncertainG = nx.Graph()
    #File = open("/Users/zhangchi/Desktop/cs690/CommunityMining/community-detection/TAP_core.txt")
    #for line in File:
    #    edgeList = line.strip().split('\t')
    #    uncertainG.add_edge(edgeList[0],edgeList[1],prob=float(edgeList[2]))
    #start = 'SSP2'
    # data 3
    #G = nx.read_gml("football_edit.gml")
    #uncertainG = addProb(G,prob=0.9,percent=0.15)
    #start = G.nodes()[random.randint(0,len(G.nodes()))]
    #start = 'Kent'
    # data 2
    uncertainG = nx.karate_club_graph()
    uncertainG = addProb(uncertainG,prob=0.9,percent=0.15)
    start = 1
    # data 1
    #uncertainG = generateUncertainGraph()
    #start = 13
    D, S, R, GList, SGR, SGList = localCommunityIdentification(uncertainG,start,100)
    #print D, S, R
    print D
    print R
    #print SGR
    GList = evaluate.sampleGraph(uncertainG,100)
    
    RList = []
    for item in GList:
        RList.append(calculateR(item,D))
    print sum(RList)/100.
    #print RList
    D2, _ = uav1.localCommunityIdentification(uncertainG,start)
    print D2
    RList2 = []
    for item in GList:
        RList2.append(calculateR(item,D2))
    print sum(RList2)/100.

    a = nx.adjacency_matrix(uncertainG,weight='prob')
    b = np.array(a.toarray())
    M,cluster = mcl(b)
    D3 = set()
    for index,item in enumerate(M[0]):
        if item > 0.98:
            D3.add(index)
    print D3
    RList3 = []
    for item in GList:
        RList3.append(calculateR(item,D3))
    print sum(RList3)/100.


def main():
    # data 4
    #uncertainG = nx.Graph()
    #File = open("/Users/zhangchi/Desktop/cs690/CommunityMining/community-detection/TAP_core.txt")
    #for line in File:
    #    edgeList = line.strip().split('\t')
    #    uncertainG.add_edge(edgeList[0],edgeList[1],prob=float(edgeList[2]))
    #start = 'SSP2'
    # data 3
    #G = nx.read_gml("football_edit.gml")
    #uncertainG = addProb(G,prob=0.9,percent=0.15)
    #start = G.nodes()[random.randint(0,len(G.nodes()))]
    #start = 'Kent'
    # data 2
    uncertainG = nx.karate_club_graph()
    uncertainG = addProb(uncertainG,prob=0.9,percent=0.15)
    A0R = []
    A1R = []
    A2R = []
    A3R = []
    for start in uncertainG.nodes():
        # data 1
        #uncertainG = generateUncertainGraph()
        #start = 13
        D, S, R, GList, SGR, SGList = localCommunityIdentification(uncertainG,start,100)
        #print D, S, R
        print D
        print R
        A0R.append(R)
        #print SGR
        GList = evaluate.sampleGraph(uncertainG,100)
        
        RList = []
        for item in GList:
            RList.append(calculateR(item,D))
        print sum(RList)/100.
        A1R.append(sum(RList)/100.)
        
        #print RList
        D2, _ = uav1.localCommunityIdentification(uncertainG,start)
        print D2
        RList2 = []
        for item in GList:
            RList2.append(calculateR(item,D2))
        print sum(RList2)/100.
        A2R.append(sum(RList2)/100.)
    
        a = nx.adjacency_matrix(uncertainG,weight='prob')
        b = np.array(a.toarray())
        M,cluster = mcl(b)
        D3 = set()
        for index,item in enumerate(M[0]):
            if item > 0.98:
                D3.add(index)
        print D3
        RList3 = []
        for item in GList:
            RList3.append(calculateR(item,D3))
        print sum(RList3)/100.
        A3R.append(sum(RList3)/100.)
        
    print A0R
    print A1R
    print A2R
    print A3R
    print sum(A0R)/len(A0R)
    print sum(A1R)/len(A1R)
    print sum(A2R)/len(A2R)
    print sum(A3R)/len(A3R)
#==============================================================================
#     # 验算计算过程
#     while True:
#         uncertainG = generateUncertainGraph()
#         D, S, R, GList, SGR, SGList = localCommunityIdentification(uncertainG,13,100)
#         print D, S, R
#         print SGR
#         RList = []
#         for item in GList:
#             RList.append(calculateR(item,D))
#         print sum(RList)/100.
#         print RList
#         #if sum(RList)/100. == float(1):
#         #    break
#         if sum(RList)/100. != R:
#             return GList, SGList
#==============================================================================
    
def sampleGraphInit(uncertainG,node):
    sampleG = nx.Graph()
    sampleG.add_node(node)
    #addNodeSet = set() # 为了建立S，所有的sample G的addNodeSet会进行union
    for otherNode in uncertainG[node]:
        probability = uncertainG[node][otherNode]['prob']
        if np.random.choice([1,0], p=[probability,1-probability]) == 1:
            sampleG.add_edge(node,otherNode)
            #addNodeSet.add(otherNode)
    sampleD = set([node])
    sampleB = {node:len(sampleG[node])}
    sampleS = set(sampleG[node].keys())
    previousRemove = set()
    R = 0
    BIn = 0
    BTotal = len(sampleG[node])
    SG = SampleGraph(sampleG,sampleD,sampleB,sampleS,previousRemove,R,BIn,BTotal)
    return SG#, addNodeSet
            
def sampleGraph(uncertainG,SG,node,checkedNodeSet):
    if node not in checkedNodeSet:
        SG.G.add_node(node)
        for otherNode in uncertainG[node]:
            if otherNode not in checkedNodeSet:
                probability = uncertainG[node][otherNode]['prob']
                if np.random.choice([1,0], p=[probability,1-probability]) == 1:
                    SG.G.add_edge(node,otherNode)
    return SG
    
def localCommunityIdentification(uncertainG,startNode,sampleNumber):
    SGList = []
    #addNodeSet = set()
    checkedNodeSet = set([startNode])
    for _ in xrange(sampleNumber):
        #tempSampleG, tempAddNodeSet = sampleGraphInit(uncertainG,startNode)
        tempSG = sampleGraphInit(uncertainG,startNode)
        SGList.append(tempSG)
        #addNodeSet = addNodeSet.union(tempAddNodeSet)
    S = set(uncertainG[startNode].keys())
    D = set([startNode])
    label = True
    R = 0
    while label:
        saveList = []
        RPrime = -float('inf')
        ShareSNodeCount = -float('inf')
        shuffleList = list(S)
        random.shuffle(shuffleList)
        for node in shuffleList:
            tempSaveList = []
            for i in xrange(sampleNumber):
                SG = SGList[i]
                SG = sampleGraph(uncertainG,SG,node,checkedNodeSet)
                SGList[i] = SG
                tempShareSNodeCount = len(set(SG.G[node].keys()).intersection(SG.S))
                if node not in SG.S: # 脱离了之前的community
                    # 更新SG的各项参数，之后确定要更新的时候再更新
                    if SG.BTotal+len(SG.G[node]) == 0:
                        if SG.R == 0: # 孤立点和孤立点（有没有link都是）
                            save = Save(False, 0, node, tempShareSNodeCount)
                        else: # 之前已经形成community，且该community没有向外的link，且添加了一个没有向外link的一个点，极少出现的情况
                        # 似乎还缺少考虑一种情况：之前已经形成community，且该community没有向外的link，添加了一个向外有link的点
                        # 和evaluate.py里已经相同处理   
                            save = Save(False, 1, node, tempShareSNodeCount)
                    else: # 之前已经形成一个community了，现在有一个孤立点
                        save = Save(False, float(SG.BIn)/float(SG.BTotal+len(SG.G[node])), node, tempShareSNodeCount)
                    tempSaveList.append(save)
                else:
                    tempSet = set(SG.G[node].keys())
                    deltaIn = len(tempSet.intersection(SG.D))
                    deltaTotal = len(tempSet) - deltaIn
                    tempB = dict(SG.B)
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
                    previousCount = 0
                    for item in removeSet:
                        count += len(set(SG.G[item].keys()).intersection(removeSet))
                        previousCount += len(set(SG.G[item].keys()).intersection(SG.previousRemove))
                    deltaPrime = count / 2 + previousCount
                    tempBIn = SG.BIn + deltaIn - deltaPrime
                    tempBTotal = SG.BTotal + deltaTotal - deltaPrime
                    if tempBTotal == 0:
                        tempRPrime = 1 # 到这里了肯定不是孤立点的情况，所以肯定是1
                    else:
                        tempRPrime = float(tempBIn)/float(tempBTotal)
                    #tempShellNodeCount = len(set(G[node].keys()).intersection(S))
                    save = Save(True, tempRPrime, node, tempShareSNodeCount)
                    save.tempB = tempB
                    save.tempBIn = tempBIn
                    save.tempBTotal = tempBTotal
                    save.removeSet = removeSet
                    tempSaveList.append(save)
            checkedNodeSet.add(node) # 循环结束，所有的sampleG都处理完了node，再把node添加上去
            changeRPrime = 0
            changeShareSNodeCount = 0
            for i in xrange(sampleNumber):
                changeRPrime += tempSaveList[i].RPrime
                changeShareSNodeCount += tempSaveList[i].shareSNodeCount
            changeRPrime = float(changeRPrime)/float(sampleNumber)
            if len(D) == 1:
                if changeShareSNodeCount > ShareSNodeCount or (changeShareSNodeCount == ShareSNodeCount and changeRPrime > RPrime):
                    saveList = tempSaveList
                    RPrime = changeRPrime
                    ShareSNodeCount = changeShareSNodeCount
            else:
                if changeRPrime > RPrime or (changeRPrime == RPrime and changeShareSNodeCount > ShareSNodeCount):
                    saveList = tempSaveList
                    RPrime = changeRPrime
                    ShareSNodeCount = changeShareSNodeCount
        if RPrime > R:
            R = RPrime
            node = saveList[0].popNode
            D.add(node)
            S.remove(node)
            dif = set(uncertainG[node]).difference(D)
            S = S.union(dif)
            for i in xrange(sampleNumber):
                if saveList[i].label == False:
                    SG = SGList[i]
                    SG.D.add(node)
                    SG.B[node] = len(SG.G[node])
                    SG.S = SG.S.union(set(SG.G[node].keys()))
                    SG.BTotal += len(SG.G[node])
                    SG.R = saveList[i].RPrime # 前面已经处理过了，不用管
#==============================================================================
#                     if SG.BTotal == 0:
#                         if SG.R == 0:
#                             SG.R = 0
#                         else:
#                             SG.R = 1
#                     else:
#                         SG.R = float(SG.BIn) / float(SG.BTotal)
#==============================================================================
                    SGList[i] = SG
                else:
                    SG = SGList[i]
                    SG.D.add(node)
                    SG.S.remove(node)
                    SG.B = {}
                    for item in saveList[i].tempB:
                        if saveList[i].tempB[item] > 0:
                            SG.B[item] = saveList[i].tempB[item]
                    difference = set(SG.G[node]).difference(SG.D)
                    if len(difference) > 0:
                        SG.B[node] = len(difference)
                        SG.S = SG.S.union(difference)
                    SG.previousRemove = SG.previousRemove.union(saveList[i].removeSet)
                    SG.R = saveList[i].RPrime
                    SG.BIn = saveList[i].tempBIn
                    SG.BTotal = saveList[i].tempBTotal
        else:
            label = False
            
#==============================================================================
#     count = 0
#     for item in SGList:
#         print len(item.G.edges())
#         count += len(item.G.edges())
#     print float(count)/float(sampleNumber)
#==============================================================================
    return D, S, R, [item.G for item in SGList], [item.R for item in SGList], SGList
            
    
            
            
def addProb(G,prob=0.9,percent=0.15):
    for a,b in G.edges():
        value = 0.5 * np.random.randn() + prob
        while value <= 0 or value > 1:
            value = 0.5 * np.random.randn() + prob
        G.edge[a][b]['prob'] = value
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
    
        G.add_edge(nodeA,nodeB,prob=value)
        count += 1
    return G
    
def generateUncertainGraph():
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
    G = addProb(G)
#==============================================================================
#     for a,b in G.edges():
#         value = 0.8
#         G.edge[a][b]['prob'] = value
#==============================================================================
    return G
    
main()