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
import paperReimplement as pR
import sys
import os

sys.path.append(os.getcwd()+'/python-louvain/')
import community as cm

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

def localCommunityIdentification(G,startNode,model,threshold=True):
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
    def helperD(node, nodeSet):
        count = 1
        for item in nodeSet:
            if item in G.edge[node]:
                count *= 1 - G.edge[node][item]['prob']
        return count
    def helperE(node, S):
        count = 1
        for item in G.edge[node]:
            if item in S:
                count *= 1 - S[item] * G.edge[node][item]['prob']
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
            if abs(tempBTotal) <= 0.000001:
                tempRPrime = 1
            else:
                tempRPrime = float(tempBIn)/float(tempBTotal)
            
            #tempSTotal = len(set(G[node].keys()).difference(D).union(S)) 
            if model == 0:
                NodeIn = helperA(node,D)#len(set(G[node].keys()).intersection(D))
                NodeShell = helperC(node,S)#helperA(node,S)#len(set(G[node].keys()).intersection(S))
                tempKPrime = float(NodeIn+NodeShell)#/float(helperB(node))#tempKPrime = float(NodeIn+NodeShell)/float(tempSTotal)
                save = Save(tempRPrime, tempKPrime, node, tempB, tempBIn, tempBTotal, removeSet)
                saveList.append(save)   
            elif model == 1:
                NodeIn = helperD(node,D)#len(set(G[node].keys()).intersection(D))
                NodeShell = helperE(node,S)#helperA(node,S)#len(set(G[node].keys()).intersection(S))
                tempKPrime = 1 - NodeIn * NodeShell#tempKPrime = float(NodeIn+NodeShell)/float(tempSTotal)
                save = Save(tempRPrime, tempKPrime, node, tempB, tempBIn, tempBTotal, removeSet)
                saveList.append(save)   
            elif model == 2:
                NodeIn = helperA(node,D)#len(set(G[node].keys()).intersection(D))
                NodeShell = helperC(node,S)#helperA(node,S)#len(set(G[node].keys()).intersection(S))
                tempKPrime = float(NodeIn+NodeShell)/float(helperB(node))
                if tempKPrime >= 0:#(1-np.exp(-len(D)*1.0/6.))*0.5:
                    save = Save(tempRPrime, tempKPrime, node, tempB, tempBIn, tempBTotal, removeSet)
                    saveList.append(save)   
            else:
                NodeIn = helperA(node,D)#len(set(G[node].keys()).intersection(D))
                NodeShell = helperC(node,S)#helperA(node,S)#len(set(G[node].keys()).intersection(S))
                tempKPrime = 2*float(NodeIn+NodeShell)-float(helperB(node))#tempKPrime = float(NodeIn+NodeShell)/float(tempSTotal)
                save = Save(tempRPrime, tempKPrime, node, tempB, tempBIn, tempBTotal, removeSet)
                saveList.append(save) 
            #if threshold is False or len(D) < 20 or (len(D) >= 20 and tempKPrime >= 0.5):
            #degree = 5.05
            #para = 1./(-np.log(1-2./degree))
            #if threshold is False or tempKPrime >= (1-np.exp(-len(D)*1.0/para))*0.5:#min(len(D),3)*0.166: #0.5 or (len(D) <= 3 and tempRPrime >= R): # 加上结果会干净很多
            #if threshold is False or tempKPrime >= min((len(D)+1)*0.5,0.5*12)/12.:
            #save = Save(tempRPrime, tempKPrime, node, tempB, tempBIn, tempBTotal, removeSet)
            #saveList.append(save)            

        saveList.sort(key=lambda save:save.RPrime,reverse=True)
        if len(D) < 4:
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
                break

        if checkLabel == False:
            label = False
            
    result = set()
    result.add(startNode)
    for item in D:
        if item != startNode:
            inValue = helperA(item,D)
            outValue = helperB(item) - inValue
            if inValue >= outValue:
                result.add(item)
    if threshold:
        return result, R#S
    else:
        return D, R#S
        
def addProbOrigin(G):
    for a,b in G.edges():
        G.edge[a][b]['prob'] = 1
        G.edge[a][b]['weight'] = 1
    return G
    
def addProb(G,prob=0.9,percent=0.15):
    for a,b in G.edges():
        value = 0.5 * np.random.randn() + prob
        while value <= 0 or value > 1:
            value = 0.5 * np.random.randn() + prob
        G.edge[a][b]['prob'] = value
        G.edge[a][b]['weight'] = 1
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
    
        G.add_edge(nodeA,nodeB,prob=value,weight=1)
        count += 1
    return G
    
#==============================================================================
# G = nx.Graph()
# G.add_edge(1,2,prob=0.9)
# G.add_edge(1,3,prob=0.9)
# G.add_edge(1,4,prob=0.9)
# G.add_edge(1,5,prob=0.9)
# G.add_edge(1,6,prob=0.9)
# G.add_edge(2,3,prob=0.9)
# G.add_edge(2,4,prob=0.9)
# G.add_edge(2,5,prob=0.9)
# G.add_edge(2,6,prob=0.9)
# G.add_edge(3,4,prob=0.9)
# G.add_edge(3,5,prob=0.9)
# G.add_edge(3,6,prob=0.9)
# G.add_edge(4,5,prob=0.9)
# G.add_edge(4,6,prob=0.9)
# G.add_edge(5,6,prob=0.9)
# 
# G.add_edge(6,7,prob=0.8)
# 
# G.add_edge(7,8,prob=0.8)
# G.add_edge(7,9,prob=0.8)
# G.add_edge(7,10,prob=0.8)
# G.add_edge(8,9,prob=0.8)
# G.add_edge(8,10,prob=0.8)
# G.add_edge(9,10,prob=0.8)
# G.add_edge(9,11,prob=0.8)
# start = 6
# result = localCommunityIdentification(G,start,0)
# print result
#==============================================================================
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
def main():
    dataList = [0]
    for dataNumber in dataList:
        print "--------------------"
        print "dataNumber: " + str(dataNumber)
        percentList = [0.4,0.3,0.2,0.1,0]#[0,0.1,0.2,0.3,0.4]
        for percentNumber in percentList:
            print "percent: " + str(percentNumber)
            R1List = []
            P1List = []
            F1List = []
            R2List = []
            P2List = []
            F2List = []
            R3List = []
            P3List = []
            F3List = []
            R4List = []
            P4List = []
            F4List = []
            R5List = []
            P5List = []
            F5List = []
            R6List = []
            P6List = []
            F6List = []
            R7List = []
            P7List = []
            F7List = []
            R8List = []
            P8List = []
            F8List = []
            R9List = []
            P9List = []
            F9List = []
            R10List = []
            P10List = []
            F10List = []
            R11List = []
            P11List = []
            F11List = []
            R12List = []
            P12List = []
            F12List = []
            testLength = 20
            for testNumber in xrange(testLength):
                #print testNumber
                if dataNumber == 0:
                    G = nx.karate_club_graph()
                elif dataNumber == 1:
                    G = nx.read_gml("football_edit.gml")
                else:
                    G = nx.Graph()
                    File = open("binary_networks/network.dat","r")
                    for line in File:
                        nodeA, nodeB = line.strip().split("\t")
                        G.add_edge(int(nodeA),int(nodeB))
                    dic = {}
                    label = {}
                    File = open("binary_networks/community.dat","r")
                    for line in File:
                        node, community = line.strip().split("\t")
                        G.node[int(node)]['value'] = int(community)
                        label[int(node)] = int(community)
                        if int(community) not in dic:
                            dic[int(community)] = set([int(node)])
                        else:
                            dic[int(community)].add(int(node))
                if percentNumber == 0:
                    G = addProbOrigin(G)
                else:
                    G = addProb(G,prob=0.8,percent=percentNumber)
#==============================================================================
#             for x in [4,5,6,10,16]:
#                 G.node[x]['club']='xxx'
#             for x in [23,24,25,27,28,31]:
#                 G.node[x]['club']='yyy'
#==============================================================================
                #for a,b in G.edges():
                #    G.edge[a][b]['prob'] = 1
                #start = 'Kent'
                dic = {}
                if dataNumber == 0:
                    labelName = 'club'
                else:
                    labelName = 'value'
                for node in G.nodes():
                    label = G.node[node][labelName]
                    if label not in dic:
                        dic[label] = set([node])
                    else:
                        dic[label].add(node)
                number = 0
                TP1 = 0
                TPFN1 = 0
                TPFP1 = 0
                TP2 = 0
                TPFN2 = 0
                TPFP2 = 0
                TP3 = 0
                TPFN3 = 0
                TPFP3 = 0
                TP4 = 0
                TPFN4 = 0
                TPFP4 = 0
                TP5 = 0
                TPFN5 = 0
                TPFP5 = 0
                TP6 = 0
                TPFN6 = 0
                TPFP6 = 0
                TP7 = 0
                TPFN7 = 0
                TPFP7 = 0
                TP8 = 0
                TPFN8 = 0
                TPFP8 = 0
                TP9 = 0
                TPFN9 = 0
                TPFP9 = 0
                
                TP10 = 0
                TPFN10 = 0
                TPFP10 = 0
                UncertainLouvainResult = cm.best_partition(G,weight='prob')
                UncertainLouvainDict = {}
                for item in UncertainLouvainResult:
                    if UncertainLouvainResult[item] not in UncertainLouvainDict:
                        UncertainLouvainDict[UncertainLouvainResult[item]] = set([item])
                    else:
                        UncertainLouvainDict[UncertainLouvainResult[item]].add(item)
                        
                TP11 = 0
                TPFN11 = 0
                TPFP11 = 0
                LouvainResult = cm.best_partition(G,weight='weight')
                LouvainDict = {}
                for item in LouvainResult:
                    if LouvainResult[item] not in LouvainDict:
                        LouvainDict[LouvainResult[item]] = set([item])
                    else:
                        LouvainDict[LouvainResult[item]].add(item)
                        
                TP12 = 0
                TPFN12 = 0
                TPFP12 = 0
                        
                for start in G.nodes():
                    #print number
                    number += 1
                    
                    result,_ = localCommunityIdentification(G,start,0)
                    label = G.node[start][labelName]
                    #print "label: " + str(label)
                    #print "node in this label: " + str(len(dic[label]))
                    #print "node actually in this label: " + str(len(result))
                    TPFN1 += len(dic[label])
                    TPFP1 += len(result)
                    for item in result:
                        #print G.node[item]
                        if G.node[item][labelName] == label:
                            TP1 += 1
                    #print "----------------------"
                    
                    result,_ = localCommunityIdentification(G,start,0,False)
                    label = G.node[start][labelName]
                    #print "label: " + str(label)
                    #print "node in this label: " + str(len(dic[label]))
                    #print "node actually in this label: " + str(len(result))
                    TPFN2 += len(dic[label])
                    TPFP2 += len(result)
                    for item in result:
                        #print G.node[item]
                        if G.node[item][labelName] == label:
                            TP2 += 1
                    #print "----------------------"
                    
                    result,_ = uA1.localCommunityIdentification(G,start)
                    label = G.node[start][labelName]
                    #print "label: " + str(label)
                    #print "node in this label: " + str(len(dic[label]))
                    #print "node actually in this label: " + str(len(result))
                    TPFN3 += len(dic[label])
                    TPFP3 += len(result)
                    for item in result:
                        #print G.node[item]
                        if G.node[item][labelName] == label:
                            TP3 += 1
                    #print "----------------------"
                            
                    result,_ = localCommunityIdentification(G,start,1)
                    label = G.node[start][labelName]
                    #print "label: " + str(label)
                    #print "node in this label: " + str(len(dic[label]))
                    #print "node actually in this label: " + str(len(result))
                    TPFN4 += len(dic[label])
                    TPFP4 += len(result)
                    for item in result:
                        #print G.node[item]
                        if G.node[item][labelName] == label:
                            TP4 += 1
                    #print "----------------------"
                    
                    result,_ = localCommunityIdentification(G,start,1,False)
                    label = G.node[start][labelName]
                    #print "label: " + str(label)
                    #print "node in this label: " + str(len(dic[label]))
                    #print "node actually in this label: " + str(len(result))
                    TPFN5 += len(dic[label])
                    TPFP5 += len(result)
                    for item in result:
                        #print G.node[item]
                        if G.node[item][labelName] == label:
                            TP5 += 1
                    #print "----------------------"
                            
                    result,_ = localCommunityIdentification(G,start,2)
                    label = G.node[start][labelName]
                    #print "label: " + str(label)
                    #print "node in this label: " + str(len(dic[label]))
                    #print "node actually in this label: " + str(len(result))
                    TPFN6 += len(dic[label])
                    TPFP6 += len(result)
                    for item in result:
                        #print G.node[item]
                        if G.node[item][labelName] == label:
                            TP6 += 1
                    #print "----------------------"
                    
                    result,_ = localCommunityIdentification(G,start,2,False)
                    label = G.node[start][labelName]
                    #print "label: " + str(label)
                    #print "node in this label: " + str(len(dic[label]))
                    #print "node actually in this label: " + str(len(result))
                    TPFN7 += len(dic[label])
                    TPFP7 += len(result)
                    for item in result:
                        #print G.node[item]
                        if G.node[item][labelName] == label:
                            TP7 += 1
                    #print "----------------------"
                            
                    result,_ = localCommunityIdentification(G,start,3)
                    label = G.node[start][labelName]
                    #print "label: " + str(label)
                    #print "node in this label: " + str(len(dic[label]))
                    #print "node actually in this label: " + str(len(result))
                    TPFN8 += len(dic[label])
                    TPFP8 += len(result)
                    for item in result:
                        #print G.node[item]
                        if G.node[item][labelName] == label:
                            TP8 += 1
                    #print "----------------------"
                    
                    result,_ = localCommunityIdentification(G,start,3,False)
                    label = G.node[start][labelName]
                    #print "label: " + str(label)
                    #print "node in this label: " + str(len(dic[label]))
                    #print "node actually in this label: " + str(len(result))
                    TPFN9 += len(dic[label])
                    TPFP9 += len(result)
                    for item in result:
                        #print G.node[item]
                        if G.node[item][labelName] == label:
                            TP9 += 1
                    #print "----------------------"
                    
                    result = UncertainLouvainDict[UncertainLouvainResult[start]]
                    label = G.node[start][labelName]
                    #print "label: " + str(label)
                    #print "node in this label: " + str(len(dic[label]))
                    #print "node actually in this label: " + str(len(result))
                    TPFN10 += len(dic[label])
                    TPFP10 += len(result)
                    for item in result:
                        #print G.node[item]
                        if G.node[item][labelName] == label:
                            TP10 += 1
                    #print "----------------------"
                    
                    result = LouvainDict[LouvainResult[start]]
                    label = G.node[start][labelName]
                    #print "label: " + str(label)
                    #print "node in this label: " + str(len(dic[label]))
                    #print "node actually in this label: " + str(len(result))
                    TPFN11 += len(dic[label])
                    TPFP11 += len(result)
                    for item in result:
                        #print G.node[item]
                        if G.node[item][labelName] == label:
                            TP11 += 1
                    #print "----------------------"
                    
                    result,_ = pR.localCommunityIdentification(G,start)
                    label = G.node[start][labelName]
                    #print "label: " + str(label)
                    #print "node in this label: " + str(len(dic[label]))
                    #print "node actually in this label: " + str(len(result))
                    TPFN12 += len(dic[label])
                    TPFP12 += len(result)
                    for item in result:
                        #print G.node[item]
                        if G.node[item][labelName] == label:
                            TP12 += 1
                    #print "**********************"
                #print "Evaluation: 正确被检索的/应该检索到的  正确被检索的/实际被检索到的"
                
                R1 = float(TP1)/float(TPFN1)
                P1 = float(TP1)/float(TPFP1)
                #print "algorithm1: "+str(R1)+'    '+str(P1)
                #print "F1 = " + str(2*R1*P1/(R1+P1))
                R1List.append(R1)
                P1List.append(P1)
                F1List.append(2*R1*P1/(R1+P1))
                
                R2 = float(TP2)/float(TPFN2)
                P2 = float(TP2)/float(TPFP2)
                #print "algorithm2: "+str(R2)+'    '+str(P2)
                #print "F1 = " + str(2*R2*P2/(R2+P2))
                R2List.append(R2)
                P2List.append(P2)
                F2List.append(2*R2*P2/(R2+P2))
                    
                R3 = float(TP3)/float(TPFN3)
                P3 = float(TP3)/float(TPFP3)
                #print "algorithm3: "+str(R3)+'    '+str(P3)
                #print "F1 = " + str(2*R3*P3/(R3+P3))
                R3List.append(R3)
                P3List.append(P3)
                F3List.append(2*R3*P3/(R3+P3))
                
                R4 = float(TP4)/float(TPFN4)
                P4 = float(TP4)/float(TPFP4)
                #print "algorithm4: "+str(R4)+'    '+str(P4)
                #print "F1 = " + str(2*R4*P4/(R4+P4))
                R4List.append(R4)
                P4List.append(P4)
                F4List.append(2*R4*P4/(R4+P4))
                
                R5 = float(TP5)/float(TPFN5)
                P5 = float(TP5)/float(TPFP5)
                #print "algorithm5: "+str(R5)+'    '+str(P5)
                #print "F1 = " + str(2*R5*P5/(R5+P5))
                R5List.append(R5)
                P5List.append(P5)
                F5List.append(2*R5*P5/(R5+P5))
                
                R6 = float(TP6)/float(TPFN6)
                P6 = float(TP6)/float(TPFP6)
                #print "algorithm6: "+str(R6)+'    '+str(P6)
                #print "F1 = " + str(2*R6*P6/(R6+P6))
                R6List.append(R6)
                P6List.append(P6)
                F6List.append(2*R6*P6/(R6+P6))
                
                R7 = float(TP7)/float(TPFN7)
                P7 = float(TP7)/float(TPFP7)
                #print "algorithm7: "+str(R7)+'    '+str(P7)
                #print "F1 = " + str(2*R7*P7/(R7+P7))
                R7List.append(R7)
                P7List.append(P7)
                F7List.append(2*R7*P7/(R7+P7))
                
                R8 = float(TP8)/float(TPFN8)
                P8 = float(TP8)/float(TPFP8)
                #print "algorithm8: "+str(R8)+'    '+str(P8)
                #print "F1 = " + str(2*R8*P8/(R8+P8))
                R8List.append(R8)
                P8List.append(P8)
                F8List.append(2*R8*P8/(R8+P8))
                
                R9 = float(TP9)/float(TPFN9)
                P9 = float(TP9)/float(TPFP9)
                #print "algorithm9: "+str(R9)+'    '+str(P9)
                #print "F1 = " + str(2*R9*P9/(R9+P9))
                R9List.append(R9)
                P9List.append(P9)
                F9List.append(2*R9*P9/(R9+P9))
                
                R10 = float(TP10)/float(TPFN10)
                P10 = float(TP10)/float(TPFP10)
                #print "algorithm10: "+str(R10)+'    '+str(P10)
                #print "F1 = " + str(2*R10*P10/(R10+P10))
                R10List.append(R10)
                P10List.append(P10)
                F10List.append(2*R10*P10/(R10+P10))
                
                R11 = float(TP11)/float(TPFN11)
                P11 = float(TP11)/float(TPFP11)
                #print "algorithm11: "+str(R11)+'    '+str(P11)
                #print "F1 = " + str(2*R11*P11/(R11+P11))
                R11List.append(R11)
                P11List.append(P11)
                F11List.append(2*R11*P11/(R11+P11))
                
                R12 = float(TP12)/float(TPFN12)
                P12 = float(TP12)/float(TPFP12)
                #print "algorithm12: "+str(R12)+'    '+str(P12)
                #print "F1 = " + str(2*R12*P12/(R12+P12))
                R12List.append(R12)
                P12List.append(P12)
                F12List.append(2*R12*P12/(R12+P12))
                
            print "Evaluation: 正确被检索的/应该检索到的  正确被检索的/实际被检索到的"
            print "uncertain R+K(threshold): "+str(sum(R1List)*1.0/testLength)+'    '+str(sum(P1List)*1.0/testLength)
            print "F1 = " + str(sum(F1List)*1.0/testLength)
            print "uncertain R+K: "+str(sum(R2List)*1.0/testLength)+'    '+str(sum(P2List)*1.0/testLength)
            print "F1 = " + str(sum(F2List)*1.0/testLength)
            print "uncertain R: "+str(sum(R3List)*1.0/testLength)+'    '+str(sum(P3List)*1.0/testLength)
            print "F1 = " + str(sum(F3List)*1.0/testLength)
            print "uncertain R+Prob(threshold): "+str(sum(R4List)*1.0/testLength)+'    '+str(sum(P4List)*1.0/testLength)
            print "F1 = " + str(sum(F4List)*1.0/testLength)
            print "uncertain R+Prob: "+str(sum(R5List)*1.0/testLength)+'    '+str(sum(P5List)*1.0/testLength)
            print "F1 = " + str(sum(F5List)*1.0/testLength)
            print "uncertain R+K/(threshold): "+str(sum(R6List)*1.0/testLength)+'    '+str(sum(P6List)*1.0/testLength)
            print "F1 = " + str(sum(F6List)*1.0/testLength)
            print "uncertain R+K/: "+str(sum(R7List)*1.0/testLength)+'    '+str(sum(P7List)*1.0/testLength)
            print "F1 = " + str(sum(F7List)*1.0/testLength)
            print "uncertain R+K-(threshold): "+str(sum(R8List)*1.0/testLength)+'    '+str(sum(P8List)*1.0/testLength)
            print "F1 = " + str(sum(F8List)*1.0/testLength)
            print "uncertain R+K-: "+str(sum(R9List)*1.0/testLength)+'    '+str(sum(P9List)*1.0/testLength)
            print "F1 = " + str(sum(F9List)*1.0/testLength)
            print "uncertain louvain: "+str(sum(R10List)*1.0/testLength)+'    '+str(sum(P10List)*1.0/testLength)
            print "F1 = " + str(sum(F10List)*1.0/testLength)
            print "original louvain: "+str(sum(R11List)*1.0/testLength)+'    '+str(sum(P11List)*1.0/testLength)
            print "F1 = " + str(sum(F11List)*1.0/testLength)
            print "original R: "+str(sum(R12List)*1.0/testLength)+'    '+str(sum(P12List)*1.0/testLength)
            print "F1 = " + str(sum(F12List)*1.0/testLength)
            print "& "+str(round(sum(R12List)*1.0/testLength,4))+'  & '+str(round(sum(P12List)*1.0/testLength,4))+'  & '+str(round(sum(F12List)*1.0/testLength,4))\
               +'  & '+str(round(sum(R3List)*1.0/testLength,4))+'  & '+str(round(sum(P3List)*1.0/testLength,4))+'  & '+str(round(sum(F3List)*1.0/testLength,4))\
               +'  & '+str(round(sum(R2List)*1.0/testLength,4))+'  & '+str(round(sum(P2List)*1.0/testLength,4))+'  & '+str(round(sum(F2List)*1.0/testLength,4))\
               +'  & '+str(round(sum(R1List)*1.0/testLength,4))+'  & '+str(round(sum(P1List)*1.0/testLength,4))+'  & '+str(round(sum(F1List)*1.0/testLength,4))\
               +'  & '+str(round(sum(R9List)*1.0/testLength,4))+'  & '+str(round(sum(P9List)*1.0/testLength,4))+'  & '+str(round(sum(F9List)*1.0/testLength,4))\
               +'  & '+str(round(sum(R8List)*1.0/testLength,4))+'  & '+str(round(sum(P8List)*1.0/testLength,4))+'  & '+str(round(sum(F8List)*1.0/testLength,4))\
               +'  & '+str(round(sum(R7List)*1.0/testLength,4))+'  & '+str(round(sum(P7List)*1.0/testLength,4))+'  & '+str(round(sum(F7List)*1.0/testLength,4))\
               +'  & '+str(round(sum(R6List)*1.0/testLength,4))+'  & '+str(round(sum(P6List)*1.0/testLength,4))+'  & '+str(round(sum(F6List)*1.0/testLength,4))\
               +'  & '+str(round(sum(R11List)*1.0/testLength,4))+'  & '+str(round(sum(P11List)*1.0/testLength,4))+'  & '+str(round(sum(F11List)*1.0/testLength,4))\
               +'  & '+str(round(sum(R10List)*1.0/testLength,4))+'  & '+str(round(sum(P10List)*1.0/testLength,4))+'  & '+str(round(sum(F10List)*1.0/testLength,4))\
               +'  \\\\ \hline'
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
#main()
    