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

class Save(object):
    def __init__(self, label, RPrime, popNode):
        self.label = label
        self.RPrime = None
        self.popNode = popNode
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

def main():
    uncertainG = generateUncertainGraph()
    print localCommunityIdentification(uncertainG,1,100)
    
def sampleGraphInit(uncertainG,node):
    sampleG = nx.Graph()
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
        for node in S:#random.shuffle(list(S)):
            tempSaveList = []
            for i in xrange(sampleNumber):
                SG = SGList[i]
                SG = sampleGraph(uncertainG,SG,node,checkedNodeSet)
                SGList[i] = SG
                if node not in SG.S: # 脱离了之前的community
                    # 更新SG的各项参数，但是R不用变（R不用重新求）,之后确定要更新的时候再更新
                    save = Save(False, float(SG.BIn)/float(SG.BTotal+len(SG.G[node])), node)
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
                        tempRPrime = 1
                    else:
                        tempRPrime = float(tempBIn)/float(tempBTotal)
                    #tempShellNodeCount = len(set(G[node].keys()).intersection(S))
                    save = Save(True, tempRPrime, node)
                    save.tempB = tempB
                    save.tempBIn = tempBIn
                    save.tempBTotal = tempBTotal
                    save.removeSet = removeSet
                    tempSaveList.append(save)
            checkedNodeSet.add(node)
            changeRPrime = 0
            for i in xrange(sampleNumber):
                changeRPrime += tempSaveList[i].RPrime
            changeRPrime = float(changeRPrime)/float(sampleNumber)
            if changeRPrime > RPrime:
                saveList = tempSaveList
                RPrime = changeRPrime
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
                    SG.R = float(SG.BIn) / float(SG.BTotal)
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
    return D, S
            
    
            
            
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
    return G
    
main()