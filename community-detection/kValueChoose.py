#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 23:16:56 2017

@author: zhangchi
"""

# research on the value of k

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

def localCommunityIdentification(G,startNode,model,stop_number,threshold=True):
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
        if len(D) < stop_number:
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
        while nodeA == nodeB or nodeB in G[nodeA]:
            nodeB = np.random.choice(nodeList, p=probabilityList)
            
        value = 0.5 * np.random.randn() + (1-prob)
        while value <= 0 or value > 1:
            value = 0.5 * np.random.randn() + (1-prob)
    
        G.add_edge(nodeA,nodeB,prob=value)#,weight=1)
        count += 1
    return G

def main():
    dataList = [0]
    for dataNumber in dataList:
        print "--------------------"
        print "dataNumber: " + str(dataNumber)
        percentList = [0,0.1,0.2,0.3,0.4]#[0.4]#[0.4,0.3,0.2,0.1,0]#[0,0.1,0.2,0.3,0.4]
        stopNumberList = [1,2,3,4,5,6]
        percentListLength = len(percentList)
        R1ListSave = [[] for _ in xrange(percentListLength)]
        P1ListSave = [[] for _ in xrange(percentListLength)]
        F1ListSave = [[] for _ in xrange(percentListLength)]
        R2ListSave = [[] for _ in xrange(percentListLength)]
        P2ListSave = [[] for _ in xrange(percentListLength)]
        F2ListSave = [[] for _ in xrange(percentListLength)]
        for index, percentNumber in enumerate(percentList):
            print "percent: " + str(percentNumber)
            for stopNumber in stopNumberList:
                R1List = []
                P1List = []
                F1List = []
                R2List = []
                P2List = []
                F2List = []
                testLength = 100
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
                            
                    for start in G.nodes():
                        #print number
                        number += 1
                        
                        result,_ = localCommunityIdentification(G,start,0,stopNumber)
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
                        
                        result,_ = localCommunityIdentification(G,start,0,stopNumber,False)
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
                        
                    
                print "Evaluation: 正确被检索的/应该检索到的  正确被检索的/实际被检索到的"
                print "uncertain R+K(threshold): "+str(sum(R1List)*1.0/testLength)+'    '+str(sum(P1List)*1.0/testLength)
                print "F1 = " + str(sum(F1List)*1.0/testLength)
                print "uncertain R+K: "+str(sum(R2List)*1.0/testLength)+'    '+str(sum(P2List)*1.0/testLength)
                print "F1 = " + str(sum(F2List)*1.0/testLength)
                print "& "+str(round(sum(R2List)*1.0/testLength,4))+'  & '+str(round(sum(P2List)*1.0/testLength,4))+'  & '+str(round(sum(F2List)*1.0/testLength,4))\
                   +'  & '+str(round(sum(R1List)*1.0/testLength,4))+'  & '+str(round(sum(P1List)*1.0/testLength,4))+'  & '+str(round(sum(F1List)*1.0/testLength,4))\
                   +'  \\\\ \hline'

                R1ListSave[index].append(sum(R1List)*1.0/testLength)
                P1ListSave[index].append(sum(P1List)*1.0/testLength)
                F1ListSave[index].append(sum(F1List)*1.0/testLength)
                R2ListSave[index].append(sum(R2List)*1.0/testLength)
                P2ListSave[index].append(sum(P2List)*1.0/testLength)
                F2ListSave[index].append(sum(F2List)*1.0/testLength)
                
    return R1ListSave, P1ListSave, F1ListSave, R2ListSave, P2ListSave, F2ListSave

               
R1ListSave, P1ListSave, F1ListSave, R2ListSave, P2ListSave, F2ListSave = main()
