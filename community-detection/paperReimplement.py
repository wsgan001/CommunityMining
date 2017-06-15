#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 23:19:22 2017

@author: zhangchi
"""

# start community detection project
# paper reimplementation

import networkx as nx
import random

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

def localCommunityIdentification(G,startNode):
    D = set([startNode])
    B = {startNode:len(G[startNode])}
    S = set(G[startNode].keys())
    previousRemove = set()
    label = True
    R = 0
    BIn = 0
    BTotal = len(G[startNode])
    while label:
        print R
        print D
        RPrime = -float('inf')
        ShellNodeCount = -float('inf')
        for node in S:
            tempSet = set(G[node].keys())
            deltaIn = len(tempSet.intersection(D))
            deltaTotal = len(tempSet) - deltaIn
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
                count += len(set(G[item].keys()).intersection(removeSet))
                previousCount += len(set(G[item].keys()).intersection(previousRemove))
            deltaPrime = count // 2 + previousCount
            tempBIn = BIn + deltaIn - deltaPrime
            tempBTotal = BTotal + deltaTotal - deltaPrime
            tempRPrime = float(tempBIn)/float(tempBTotal)
            tempShellNodeCount = len(set(G[node].keys()).intersection(S))
            if len(D) == 1:
                if tempShellNodeCount > ShellNodeCount or (tempShellNodeCount == ShellNodeCount and tempRPrime > RPrime):
                    RPrime = tempRPrime
                    ShellNodeCount = tempShellNodeCount
                    popNodeList = [node]
                    saveBList = [tempB] #还需要再处理，去掉已经变成0的元素 可能需要写成[dict(tempB)]
                    saveBInList = [tempBIn]
                    saveBTotalList = [tempBTotal]
                    saveRemoveSetList = [removeSet]
                elif tempRPrime == RPrime and tempShellNodeCount == ShellNodeCount:
                    popNodeList.append(node)
                    saveBList.append(tempB)
                    saveBInList.append(tempBIn)
                    saveBTotalList.append(tempBTotal)
                    saveRemoveSetList.append(removeSet)
            else:
                if tempRPrime > RPrime or (tempRPrime == RPrime and tempShellNodeCount > ShellNodeCount):
                    RPrime = tempRPrime
                    ShellNodeCount = tempShellNodeCount
                    popNodeList = [node]
                    saveBList = [tempB] #还需要再处理，去掉已经变成0的元素 可能需要写成[dict(tempB)]
                    saveBInList = [tempBIn]
                    saveBTotalList = [tempBTotal]
                    saveRemoveSetList = [removeSet]
                elif tempRPrime == RPrime and tempShellNodeCount == ShellNodeCount:
                    popNodeList.append(node)
                    saveBList.append(tempB)
                    saveBInList.append(tempBIn)
                    saveBTotalList.append(tempBTotal)
                    saveRemoveSetList.append(removeSet)
        if RPrime > R:# or (RPrime > 0.98 * R and ShellNodeCount >= 2):
            print popNodeList
            print RPrime
            print ShellNodeCount
            index = random.randint(0,len(popNodeList)-1)
            popNode = popNodeList[index]
            saveB = saveBList[index]
            saveBIn = saveBInList[index]
            saveBTotal = saveBTotalList[index]
            saveRemoveSet = saveRemoveSetList[index]
            D.add(popNode)
            S.remove(popNode)
            B = {}
            for item in saveB:
                if saveB[item] > 0:
                    B[item] = saveB[item]
            difference = set(G[popNode]).difference(D)
            if len(difference) > 0:
                B[popNode] = len(difference)
                S = S.union(difference)
            previousRemove = previousRemove.union(saveRemoveSet)
            R = RPrime
            BIn = saveBIn
            BTotal = saveBTotal
        else:
            label = False
    return D, S
    
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
# start = 10
#==============================================================================
#==============================================================================
# G = generateGraph()
# start = 7
# result = iterativeExpansion(G,start)
# print result
#==============================================================================
G = nx.karate_club_graph() # 2被分错了，start=1时[24, 25, 28, 31]被单独了出来，但是总体很不错，有时候也会独立[16, 10, 4, 5, 6]
#当start=7时 [16, 10, 4, 5, 6]被独立
start = 1
result = iterativeExpansion(G,start)
print result
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
        
    