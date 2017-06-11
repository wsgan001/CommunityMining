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
        if RPrime > R:
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
    return
    
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
start = 13
localCommunityIdentification(G,start)

            
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
        
    