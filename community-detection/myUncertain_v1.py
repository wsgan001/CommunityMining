#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 16:30:33 2017

@author: zhangchi
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 15:44:54 2017

@author: zhangchi
"""

# start community detection project
# paper reimplementation

import networkx as nx
import numpy as np
import random
import uncertainAlgorithm_v1 as uA1

class Save(object):
    def __init__(self, RPrime, KPrime, popNode, tempB, tempBIn, tempBTotal, removeSet):
        self.RPrime = RPrime
        self.KPrime = KPrime
        self.popNode = popNode
        self.tempB = tempB
        self.tempBIn = tempBIn
        self.tempBTotal = tempBTotal
        self.removeSet = removeSet   

def generateGraph():
    G = nx.random_partition_graph([30,50],0.2,0.02)
    return G
    
def iterativeExpansion(G,startNode):
    commnutyList = []
    community, shell = localCommunityIdentification(G,startNode)
    commnutyList.append(community)
    while len(shell) > 0:
        startNode = list(shell)[random.randint(0,len(shell)-1)]
        community, shellPrime = localCommunityIdentification(G,startNode)
        commnutyList.append(community)
        shell = shell.difference(community)
        for item in commnutyList:
            shellPrime = shellPrime.difference(item)
        shell = shell.union(shellPrime)
    print "**************************"
    label = True
    print commnutyList
    print "**************************"
    while label:
        label = False
        temp = []
        stopIndex = []
        for i in xrange(len(commnutyList)):
            tempLabel = True
            if i not in stopIndex:
                for j in xrange(i+1,len(commnutyList)):
                    lengthA = len(commnutyList[i])
                    lengthB = len(commnutyList[j])
                    if len(commnutyList[i].intersection(commnutyList[j])) > 0.8 * min(lengthA,lengthB):
                        label = True
                        tempLabel = False
                        temp.append(commnutyList[i].union(commnutyList[j]))
                        stopIndex.append(j)
                        break
                if tempLabel:
                    temp.append(commnutyList[i])
        commnutyList = temp
    return commnutyList

def localCommunityIdentification(G,startNode,threshold=True):
    def helperA(node, nodeSet):
        count = 0
        for item in nodeSet:
            if item in G.edge[node]:
                count += G.edge[node][item]['prob']
        return count
    def helperB(node):
        count = 0
        for item in G.edge[node]:
            count += G.edge[node][item]['prob']
        return count
    def helperC(node, S):
        count = 0
        for item in G.edge[node]:
            if item in S:
                count += S[item] * G.edge[node][item]['prob']
        return count
    D = set([startNode])
    B = {startNode:len(G[startNode])}
    #S = set(G[startNode].keys())
    S = {}
    for node in G[startNode].keys():
        S[node] = G.edge[startNode][node]['prob']
    previousRemove = set()
    label = True
    R = 0
    K = 0
    BIn = 0
    BTotal = helperB(startNode)#len(G[startNode])
    while label:
        #print R
        #print BIn
        #print BTotal
        #print D
        saveList = []
        for node in S:
            tempSet = set(G[node].keys())
            deltaIn = helperA(node,D)#len(tempSet.intersection(D))
            deltaTotal = helperB(node) - deltaIn#len(tempSet) - deltaIn
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
            previousCount = 0
            for item in removeSet:
                count += helperA(item,removeSet)#len(set(G[item].keys()).intersection(removeSet))
                previousCount += helperA(item,previousRemove)#len(set(G[item].keys()).intersection(previousRemove))
            deltaPrime = count / 2 + previousCount
            tempBIn = BIn + deltaIn - deltaPrime
            tempBTotal = BTotal + deltaTotal - deltaPrime
            tempRPrime = float(tempBIn)/float(tempBTotal)
            
            #tempSTotal = len(set(G[node].keys()).difference(D).union(S)) 
            
            NodeIn = helperA(node,D)#len(set(G[node].keys()).intersection(D))
            NodeShell = helperC(node,S)#helperA(node,S)#len(set(G[node].keys()).intersection(S))
            tempKPrime = float(NodeIn+NodeShell)/float(helperB(node))
            #tempKPrime = float(NodeIn+NodeShell)/float(tempSTotal)
            
            if threshold is False or tempKPrime >= (1-np.exp(-len(D)/2.))*0.5:#min(len(D),3)*0.166: #0.5 or (len(D) <= 3 and tempRPrime >= R): # 加上结果会干净很多
                save = Save(tempRPrime, tempKPrime, node, tempB, tempBIn, tempBTotal, removeSet)
                saveList.append(save)            

        saveList.sort(key=lambda save:save.RPrime,reverse=True)
        saveList.sort(key=lambda save:save.KPrime,reverse=True)
        checkLabel = False
        for save in saveList:
            if save.RPrime > R:# or (RPrime > 0.98 * R and ShellNodeCount >= 2):
                popNode = save.popNode
                saveB = save.tempB
                saveBIn = save.tempBIn
                saveBTotal = save.tempBTotal
                saveRemoveSet = save.removeSet
                D.add(popNode)
                S.pop(popNode)#S.remove(popNode)
                # update S
                for item in G.edge[popNode]:
                    if item in S:
                        S[item] = 1 - (1 - S[item]) * (1 - G.edge[popNode][item]['prob'])
                ###############
                B = {}
                for item in saveB:
                    if saveB[item] > 0:
                        B[item] = saveB[item]
                difference = set(G[popNode]).difference(D)
                if len(difference) > 0:
                    B[popNode] = len(difference)
                    #S = S.union(difference)
                    for item in difference:
                        S[item] = G.edge[popNode][item]['prob']
                previousRemove = previousRemove.union(saveRemoveSet)
                R = save.RPrime
                K = save.KPrime
                BIn = saveBIn
                BTotal = saveBTotal
                checkLabel = True

        if checkLabel == False:
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
    
#==============================================================================
# G = nx.read_gml("network.gml")
# start = 0
# result = localCommunityIdentification(G,start)
# print result
# print len(result[0])
# dic = {}
# for item in G.nodes():
#     label = int(G.node[item]['c'][2])
#     if label not in dic:
#         dic[label] = set([item])
#     else:
#         dic[label].add(item)
# print len(dic[int(G.node[start]['c'][2])])
# intersection = result[0].intersection(dic[int(G.node[start]['c'][2])])
# print len(intersection)
#==============================================================================
    
#==============================================================================
# G = nx.Graph()
# G.add_edge(1,2)
# G.add_edge(1,3)
# G.add_edge(1,4)
# G.add_edge(2,3)
# G.add_edge(2,4)
# G.add_edge(2,13)
# G.add_edge(3,4)
# G.add_edge(3,7)
# G.add_edge(3,13)
# G.add_edge(4,9)
# G.add_edge(4,13)
# G.add_edge(5,6)
# G.add_edge(5,7)
# G.add_edge(5,8)
# G.add_edge(5,13)
# G.add_edge(6,7)
# G.add_edge(6,8)
# G.add_edge(6,10)
# G.add_edge(6,13)
# G.add_edge(7,8)
# G.add_edge(7,13)
# G.add_edge(9,10)
# G.add_edge(9,11)
# G.add_edge(9,12)
# G.add_edge(10,11)
# G.add_edge(10,12)
# G.add_edge(11,12)
# G.add_edge(11,13)
# start = 12
# print localCommunityIdentification(G,start)[0]
#==============================================================================
#==============================================================================
# G = generateGraph()
# start = 7
# #result = iterativeExpansion(G,start)
# result,_ = localCommunityIdentification(G,start)
# print result
#==============================================================================
# #==============================================================================
# G = nx.karate_club_graph() # 2被分错了，start=1时[24, 25, 28, 31]被单独了出来，但是总体很不错，有时候也会独立[16, 10, 4, 5, 6]
# #当start=7时 [16, 10, 4, 5, 6]被独立
# start = 1
# result = iterativeExpansion(G,start)
# print result
#==============================================================================
#G = nx.florentine_families_graph()
#start = 'Strozzi'
#==============================================================================
# G = nx.read_gml("football_edit.gml") # value = 10这一组被分成了两组
# start = 'Kent'
# #print len(localCommunityIdentification(G,start)[0])
# result = iterativeExpansion(G,start)
# print result
# for temp in result:
#     for item in temp:
#         print G.node[item]
#     print '*******************'
#==============================================================================
#==============================================================================
# G = nx.read_gml("football_edit.gml")
# G = addProb(G,prob=0.8,percent=0.35)
# #for a,b in G.edges():
# #    G.edge[a][b]['prob'] = 1
# #start = 'Kent'
# dic = {}
# for node in G.nodes():
#     label = G.node[node]['value']
#     if label not in dic:
#         dic[label] = set([node])
#     else:
#         dic[label].add(node)
# number = 0
# TP1 = 0
# TPFN1 = 0
# TPFP1 = 0
# TP2 = 0
# TPFN2 = 0
# TPFP2 = 0
# TP3 = 0
# TPFN3 = 0
# TPFP3 = 0
# for start in G.nodes():
#     print number
#     number += 1
#     
#     result,_ = localCommunityIdentification(G,start)
#     label = G.node[start]['value']
#     print "label: " + str(label)
#     print "node in this label: " + str(len(dic[label]))
#     print "node actually in this label: " + str(len(result))
#     TPFN1 += len(dic[label])
#     TPFP1 += len(result)
#     for item in result:
#         print G.node[item]
#         if G.node[item]['value'] == label:
#             TP1 += 1
#     print "----------------------"
#     
#     result,_ = localCommunityIdentification(G,start,False)
#     label = G.node[start]['value']
#     print "label: " + str(label)
#     print "node in this label: " + str(len(dic[label]))
#     print "node actually in this label: " + str(len(result))
#     TPFN3 += len(dic[label])
#     TPFP3 += len(result)
#     for item in result:
#         print G.node[item]
#         if G.node[item]['value'] == label:
#             TP3 += 1
#     print "----------------------"
#     
#     result,_ = uA1.localCommunityIdentification(G,start)
#     label = G.node[start]['value']
#     print "label: " + str(label)
#     print "node in this label: " + str(len(dic[label]))
#     print "node actually in this label: " + str(len(result))
#     TPFN2 += len(dic[label])
#     TPFP2 += len(result)
#     for item in result:
#         print G.node[item]
#         if G.node[item]['value'] == label:
#             TP2 += 1
#     print "**********************"
# print "Evaluation: 正确被检索的/应该检索到的  正确被检索的/实际被检索到的"
# R1 = float(TP1)/float(TPFN1)
# P1 = float(TP1)/float(TPFP1)
# print "algorithm1: "+str(R1)+'    '+str(P1)
# print "F1 = " + str(2*R1*P1/(R1+P1))
# 
# R3 = float(TP3)/float(TPFN3)
# P3 = float(TP3)/float(TPFP3)
# print "algorithm3: "+str(R3)+'    '+str(P3)
# print "F1 = " + str(2*R3*P3/(R3+P3))
# 
# R2 = float(TP2)/float(TPFN2)
# P2 = float(TP2)/float(TPFP2)
# print "algorithm2: "+str(R2)+'    '+str(P2)
# print "F1 = " + str(2*R2*P2/(R2+P2))
#==============================================================================
    
            
#==============================================================================
# G = nx.Graph()
# G.add_edge(1,4)
# G.add_edge(1,3)
# G.add_edge(2,3)
# G.add_edge(2,4)
# G.add_edge(3,4)
# G.add_edge(4,5)
# G.add_edge(4,6)
# D = set([1,2,4])
# B = {1:1,2:1,4:3}
# S = set([3,5,6])
# label = True
# R = 0
# while label:
#     RPrime = -float('inf')
#     for node in S:
#         tempSet = set(G[node].keys())
#         deltaIn = len(tempSet.intersection(D))
#         deltaTotal = len(tempSet) - deltaIn
#         tempB = dict(B)
#         removeSet = set()
#         tempLabel = True
#         for item in tempSet:
#             if item in tempB:
#                 tempB[item] -= 1
#                 if tempB[item] == 0:
#                     removeSet.add(item)
#             else:
#                 tempLabel = False
#         if tempLabel:
#             removeSet.add(node)
#         count = 0
#         for item in removeSet:
#             count += len(set(G[item].keys()).intersection(removeSet))
#         deltaPrime = count // 2
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
        
    