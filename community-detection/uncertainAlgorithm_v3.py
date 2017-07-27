#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 18:21:23 2017

@author: zhangchi
"""

# local community detection with uncertainty

import networkx as nx
import numpy as np
import random
from evaluate import calculateR, calculateUncertainR
import evaluate
import uncertainAlgorithm_v1 as uav1
import os, sys
import cmty
import myUncertain_v1 as mU1
import paperReimplement as pR

sys.path.append(os.getcwd()+'/python_mcl-master/mcl/')
from mcl_clustering import mcl

sys.path.append(os.getcwd()+'/python-louvain/')
import community

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

def evaluationSampleR():
    percentList = [0,0.1,0.2,0.3,0.4]
    for percentNumber in percentList:
        print "percent = " + str(percentNumber)
        A0RList = []
        A1RList = []
        A2RList = []
        A3RList = []
        A4RList = []
        A5RList = []
        A10RList = []
        A11RList = []
        testLength = 40
        for testNumber in xrange(testLength):
#==============================================================================
#         uncertainG = nx.Graph()
#         File = open("/Users/zhangchi/Desktop/cs690/CommunityMining/community-detection/TAP_core.txt")
#         for line in File:
#             edgeList = line.strip().split('\t')
#             uncertainG.add_edge(edgeList[0],edgeList[1],prob=float(edgeList[2]))
#==============================================================================
            #start = 'SSP2'
            # data 3
            G = nx.Graph()
            File = open("binary_networks/network.dat","r")
            for line in File:
                nodeA, nodeB = line.strip().split("\t")
                G.add_edge(int(nodeA),int(nodeB))
            dic = {}
            label = {}
            File = open("binary_networks/community.dat","r")
            for line in File:
                node, communitys = line.strip().split("\t")
                G.node[int(node)]['value'] = int(communitys)
                label[int(node)] = int(communitys)
                if int(communitys) not in dic:
                    dic[int(communitys)] = set([int(node)])
                else:
                    dic[int(communitys)].add(int(node))
            #G = nx.read_gml("football_edit.gml")
            #G = nx.read_gml("dolphin_edit.gml")
            G = nx.karate_club_graph()
            if percentNumber == 0:
                uncertainG = addProbOrigin(G)
            else: 
                uncertainG = addProb(G,prob=0.8,percent=percentNumber)
            #start = G.nodes()[random.randint(0,len(G.nodes()))]
            #start = 'Kent'a
            # data 2
            #uncertainG = nx.karate_club_graph()
            #uncertainG = nx.random_partition_graph([10]*8,0.4,0.02)
            #uncertainG = addProb(uncertainG,prob=0.9,percent=0.15)
            A0R = []
            A1R = []
            A2R = []
            A3R = []
            A4R = []
            A5R = []
            A10R = []
            A11R = []
        
            GList = evaluate.sampleGraph(uncertainG,100)
            #print "finish sampling"
            testList = list(uncertainG.nodes())
            random.shuffle(testList)
            testList = testList[:300]
            for start in testList:#uncertainG.nodes():
                
                D0, _ = pR.localCommunityIdentification(G,start)
                #print D0
                RList0 = []
                for item in GList:
                    RList0.append(calculateR(item,D0))
                #print sum(RList0)/100.
                A0R.append(sum(RList0)/100.)
                
                D1, _ = uav1.localCommunityIdentification(uncertainG,start)
                #print D1
                RList1 = []
                for item in GList:
                    RList1.append(calculateR(item,D1))
                #print sum(RList1)/100.
                A1R.append(sum(RList1)/100.)
                
                D2, _ = mU1.localCommunityIdentification(uncertainG,start,0,False)
                #print D2
                RList2 = []
                for item in GList:
                    RList2.append(calculateR(item,D2))
                #print sum(RList2)/100.
                A2R.append(sum(RList2)/100.)
                
                D3, _ = mU1.localCommunityIdentification(uncertainG,start,0)
                #print D3
                RList3 = []
                for item in GList:
                    RList3.append(calculateR(item,D3))
                #print sum(RList3)/100.
                A3R.append(sum(RList3)/100.)
                
                
                D10, _ = mU1.localCommunityIdentification(uncertainG,start,2,False) #karate上非常不稳定，有时很好有时很不好
                #print D10
                RList10 = []
                for item in GList:
                    RList10.append(calculateR(item,D10))
                #print sum(RList10)/100.
                A10R.append(sum(RList10)/100.)
                
                D11, _ = mU1.localCommunityIdentification(uncertainG,start,3,False)
                #print D11
                RList11 = []
                for item in GList:
                    RList11.append(calculateR(item,D11))
                #print sum(RList11)/100.
                A11R.append(sum(RList11)/100.)
        
                
            # Louvain Community Detection weighted version
            A4Result = community.best_partition(uncertainG,weight='weight')
            #print "finish algorithm"
            A4Dict = {}
            for item in A4Result:
                if A4Result[item] not in A4Dict:
                    A4Dict[A4Result[item]] = set([item])
                else:
                    A4Dict[A4Result[item]].add(item)
            #print "finish calculation"
            for start in testList:#uncertainG.nodes():
                RList4 = []
                D4 = A4Dict[A4Result[start]]
                for item in GList:
                    RList4.append(calculateR(item,D4))
                A4R.append(sum(RList4)/100.)
                
            # Louvain Community Detection
            A5Result = community.best_partition(uncertainG,weight='prob')
            #print "finish algorithm"
            A5Dict = {}
            for item in A5Result:
                if A5Result[item] not in A5Dict:
                    A5Dict[A5Result[item]] = set([item])
                else:
                    A5Dict[A5Result[item]].add(item)
            #print "finish calculation"
            for start in testList:#uncertainG.nodes():
                RList5 = []
                D5 = A5Dict[A5Result[start]]
                for item in GList:
                    RList5.append(calculateR(item,D5))
                A5R.append(sum(RList5)/100.)
            
            A0RList.append(sum(A0R)/len(A0R))
            A1RList.append(sum(A1R)/len(A1R))
            A2RList.append(sum(A2R)/len(A2R))
            A3RList.append(sum(A3R)/len(A3R))
            A4RList.append(sum(A4R)/len(A4R))
            A5RList.append(sum(A5R)/len(A5R))
            A10RList.append(sum(A10R)/len(A10R))
            A11RList.append(sum(A11R)/len(A11R))
        
        print "original R: " + str(sum(A0RList)*1.0/testLength)
        print "uncertain R: " + str(sum(A1RList)*1.0/testLength)
        print "uncertain R+K: " + str(sum(A2RList)*1.0/testLength)
        print "uncertain R+K(Examination): " + str(sum(A3RList)*1.0/testLength)
        print "original louvain: " + str(sum(A4RList)*1.0/testLength)
        print "uncertain louvain: " + str(sum(A5RList)*1.0/testLength)
        print "uncertain R+K/(Examination): " + str(sum(A10RList)*1.0/testLength)
        print "uncertain R+K-(Examination): " + str(sum(A11RList)*1.0/testLength)
        
        print "&  " + str(round(sum(A0RList)*1.0/testLength,4))\
            + "&  " + str(round(sum(A1RList)*1.0/testLength,4))\
            + "&  " + str(round(sum(A2RList)*1.0/testLength,4))\
            + "&  " + str(round(sum(A3RList)*1.0/testLength,4))\
            + "&  " + str(round(sum(A4RList)*1.0/testLength,4))\
            + "&  " + str(round(sum(A5RList)*1.0/testLength,4))+'  \\\\ \hline'
            
def evaluationUncertainR():
    percentList = [0,0.1,0.2,0.3,0.4]
    for percentNumber in percentList:
        print "percent = " + str(percentNumber)
        A0RList = []
        A1RList = []
        A2RList = []
        A3RList = []
        A4RList = []
        A5RList = []
        A10RList = []
        A11RList = []
        testLength = 20
        for testNumber in xrange(testLength):
#==============================================================================
#         uncertainG = nx.Graph()
#         File = open("/Users/zhangchi/Desktop/cs690/CommunityMining/community-detection/TAP_core.txt")
#         for line in File:
#             edgeList = line.strip().split('\t')
#             uncertainG.add_edge(edgeList[0],edgeList[1],prob=float(edgeList[2]))
#==============================================================================
            #start = 'SSP2'
            # data 3
            G = nx.Graph()
            File = open("binary_networks/network.dat","r")
            for line in File:
                nodeA, nodeB = line.strip().split("\t")
                G.add_edge(int(nodeA),int(nodeB))
            dic = {}
            label = {}
            File = open("binary_networks/community.dat","r")
            for line in File:
                node, communitys = line.strip().split("\t")
                G.node[int(node)]['value'] = int(communitys)
                label[int(node)] = int(communitys)
                if int(communitys) not in dic:
                    dic[int(communitys)] = set([int(node)])
                else:
                    dic[int(communitys)].add(int(node))
            #G = nx.read_gml("football_edit.gml")
            #G = nx.read_gml("dolphin_edit.gml")
            #G = nx.karate_club_graph()
            if percentNumber == 0:
                uncertainG = addProbOrigin(G)
            else: 
                uncertainG = addProb(G,prob=0.8,percent=percentNumber)
            #start = G.nodes()[random.randint(0,len(G.nodes()))]
            #start = 'Kent'a
            # data 2
            #uncertainG = nx.karate_club_graph()
            #uncertainG = nx.random_partition_graph([10]*8,0.4,0.02)
            #uncertainG = addProb(uncertainG,prob=0.9,percent=0.15)
            A0R = []
            A1R = []
            A2R = []
            A3R = []
            A4R = []
            A5R = []
            A10R = []
            A11R = []
        
            GList = evaluate.sampleGraph(uncertainG,100)
            #print "finish sampling"
            testList = list(uncertainG.nodes())
            random.shuffle(testList)
            testList = testList[:300]
            for start in testList:#uncertainG.nodes():
                
                D0, _ = pR.localCommunityIdentification(G,start)
                A0R.append(calculateUncertainR(G,D0))
                
                D1, R1 = uav1.localCommunityIdentification(uncertainG,start)
                if abs(R1 - calculateUncertainR(G,D1)) > 10 ** (-3):
                    print "*********"
                    print D1
                    print R1
                    print calculateUncertainR(G,D1)
                A1R.append(calculateUncertainR(G,D1))
                
                D2, R2 = mU1.localCommunityIdentification(uncertainG,start,0,False)
                if abs(R2 - calculateUncertainR(G,D2)) > 10 ** (-3):
                    print "+++++++++"
                    print D2
                    print R2
                    print calculateUncertainR(G,D2)
                A2R.append(calculateUncertainR(G,D2))
                
                D3, _ = mU1.localCommunityIdentification(uncertainG,start,0)
                A3R.append(calculateUncertainR(G,D3))
                
                D10, R10 = mU1.localCommunityIdentification(uncertainG,start,2,False) #karate上非常不稳定，有时很好有时很不好
                if abs(R10 - calculateUncertainR(G,D10)) > 10 ** (-3):
                    print "----------"
                    print D10
                    print R10
                    print calculateUncertainR(G,D10)
                A10R.append(calculateUncertainR(G,D10))
                
                D11, R11 = mU1.localCommunityIdentification(uncertainG,start,3,False)
                if abs(R11 - calculateUncertainR(G,D11)) > 10 ** (-3):
                    print "&&&&&&&&&&&"
                    print D11
                    print R11
                    print calculateUncertainR(G,D11)
                A11R.append(calculateUncertainR(G,D11))
        
                
            # Louvain Community Detection weighted version
            A4Result = community.best_partition(uncertainG,weight='weight')
            #print "finish algorithm"
            A4Dict = {}
            for item in A4Result:
                if A4Result[item] not in A4Dict:
                    A4Dict[A4Result[item]] = set([item])
                else:
                    A4Dict[A4Result[item]].add(item)
            #print "finish calculation"
            for start in testList:#uncertainG.nodes():
                RList4 = []
                D4 = A4Dict[A4Result[start]]
                for item in GList:
                    RList4.append(calculateR(item,D4))
                A4R.append(sum(RList4)/100.)
                
            # Louvain Community Detection
            A5Result = community.best_partition(uncertainG,weight='prob')
            #print "finish algorithm"
            A5Dict = {}
            for item in A5Result:
                if A5Result[item] not in A5Dict:
                    A5Dict[A5Result[item]] = set([item])
                else:
                    A5Dict[A5Result[item]].add(item)
            #print "finish calculation"
            for start in testList:#uncertainG.nodes():
                RList5 = []
                D5 = A5Dict[A5Result[start]]
                for item in GList:
                    RList5.append(calculateR(item,D5))
                A5R.append(sum(RList5)/100.)
            
            A0RList.append(sum(A0R)/len(A0R))
            A1RList.append(sum(A1R)/len(A1R))
            A2RList.append(sum(A2R)/len(A2R))
            A3RList.append(sum(A3R)/len(A3R))
            A4RList.append(sum(A4R)/len(A4R))
            A5RList.append(sum(A5R)/len(A5R))
            A10RList.append(sum(A10R)/len(A10R))
            A11RList.append(sum(A11R)/len(A11R))
        
        print "original R: " + str(sum(A0RList)*1.0/testLength)
        print "uncertain R: " + str(sum(A1RList)*1.0/testLength)
        print "uncertain R+K: " + str(sum(A2RList)*1.0/testLength)
        print "uncertain R+K(Examination): " + str(sum(A3RList)*1.0/testLength)
        print "original louvain: " + str(sum(A4RList)*1.0/testLength)
        print "uncertain louvain: " + str(sum(A5RList)*1.0/testLength)
        print "uncertain R+K/(Examination): " + str(sum(A10RList)*1.0/testLength)
        print "uncertain R+K-(Examination): " + str(sum(A11RList)*1.0/testLength)
        
        print "&  " + str(round(sum(A0RList)*1.0/testLength,4))\
            + "&  " + str(round(sum(A1RList)*1.0/testLength,4))\
            + "&  " + str(round(sum(A2RList)*1.0/testLength,4))\
            + "&  " + str(round(sum(A3RList)*1.0/testLength,4))\
            + "&  " + str(round(sum(A4RList)*1.0/testLength,4))\
            + "&  " + str(round(sum(A5RList)*1.0/testLength,4))+'  \\\\ \hline'
    
#==============================================================================
#     print A0R
#     print A1R
#     print A2R
#     print A3R
#     print A4R
#     print A5R
#     print A10R
#     print A11R
#     print sum(A0R)/len(A0R)
#     print sum(A1R)/len(A1R)
#     print sum(A2R)/len(A2R)
#     print sum(A3R)/len(A3R)
#     print sum(A4R)/len(A4R)
#     print sum(A5R)/len(A5R)
#     print sum(A10R)/len(A10R)
#     print sum(A11R)/len(A11R)
#==============================================================================
        
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
    uncertainG = addProb(uncertainG,prob=0.8,percent=0.15)
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
#==============================================================================
#     uncertainG = nx.Graph()
#     File = open("/Users/zhangchi/Desktop/cs690/CommunityMining/community-detection/TAP_core.txt")
#     for line in File:
#         edgeList = line.strip().split('\t')
#         uncertainG.add_edge(edgeList[0],edgeList[1],prob=float(edgeList[2]))
#==============================================================================
    #start = 'SSP2'
    # data 3
    #G = nx.read_gml("football_edit.gml")
    #G = nx.read_gml("dolphin_edit.gml")
    G = nx.karate_club_graph()
    #uncertainG = addProb(G,prob=0.75,percent=0.25)
    uncertainG = addProb(G,prob=0.8,percent=0.25)
    #start = G.nodes()[random.randint(0,len(G.nodes()))]
    #start = 'Kent'a
    # data 2
    #uncertainG = nx.karate_club_graph()
    #uncertainG = nx.random_partition_graph([10]*8,0.4,0.02)
    #uncertainG = addProb(uncertainG,prob=0.9,percent=0.15)
    A0R = []
    A1R = []
    A2R = []
    A3R = []
    A4R = []
    A5R = []
    A6R = []
    A7R = []
    A8R = []
    A9R = []
    A10R = []
    A11R = []
    A1Dict = {}
    GList = evaluate.sampleGraph(uncertainG,100)
    print "finish sampling"
    testList = list(uncertainG.nodes())
    random.shuffle(testList)
    testList = testList[:300]
    for start in testList:#uncertainG.nodes():
        # data 1
        #uncertainG = generateUncertainGraph()
        #start = 13
#==============================================================================
#         D, S, R, _, SGR, SGList = localCommunityIdentification(uncertainG,start,100)
#         A1Dict[start] = D
#         #print D, S, R
#         print D
#         print R
#         A0R.append(R)
#         #print SGR
#         if R == 0:
#             #return D, S, R, _, SGR, SGList, uncertainG, GList
#             return GList, "", uncertainG
#         
#         RList = []
#         for item in GList:
#             RList.append(calculateR(item,D))
#         print sum(RList)/100.
#         A1R.append(sum(RList)/100.)
#         
#         if sum(RList)/100. == 0:
#             return D, S, R, _, SGR, SGList, uncertainG, GList
#==============================================================================
        
        #print RList
        D2, _ = uav1.localCommunityIdentification(uncertainG,start)
        #D2, _ = mU1.localCommunityIdentification(uncertainG,start)
        print D2
        RList2 = []
        for item in GList:
            RList2.append(calculateR(item,D2))
        print sum(RList2)/100.
        A2R.append(sum(RList2)/100.)
        
        D6, _ = mU1.localCommunityIdentification(uncertainG,start,0)
        print D6
        RList6 = []
        for item in GList:
            RList6.append(calculateR(item,D6))
        print sum(RList6)/100.
        A6R.append(sum(RList6)/100.)
        
        D7, _ = mU1.localCommunityIdentification(uncertainG,start,0,False)
        print D7
        RList7 = []
        for item in GList:
            RList7.append(calculateR(item,D7))
        print sum(RList7)/100.
        A7R.append(sum(RList7)/100.)
        
        D8, _ = mU1.localCommunityIdentification(uncertainG,start,1)
        print D8
        RList8 = []
        for item in GList:
            RList8.append(calculateR(item,D8))
        print sum(RList8)/100.
        A8R.append(sum(RList8)/100.)
        
        D9, _ = mU1.localCommunityIdentification(uncertainG,start,1,False)
        print D9
        RList9 = []
        for item in GList:
            RList9.append(calculateR(item,D9))
        print sum(RList9)/100.
        A9R.append(sum(RList9)/100.)
        
        D10, _ = mU1.localCommunityIdentification(uncertainG,start,2) #karate上非常不稳定，有时很好有时很不好
        print D10
        RList10 = []
        for item in GList:
            RList10.append(calculateR(item,D10))
        print sum(RList10)/100.
        A10R.append(sum(RList10)/100.)
        
        D11, _ = mU1.localCommunityIdentification(uncertainG,start,2,False)
        print D11
        RList11 = []
        for item in GList:
            RList11.append(calculateR(item,D11))
        print sum(RList11)/100.
        A11R.append(sum(RList11)/100.)
    
#==============================================================================
#         # MCL algorithm
#         a = nx.adjacency_matrix(uncertainG,weight='prob')
#         b = np.array(a.toarray())
#         M,cluster = mcl(b)
#         D3 = set()
#         for index,item in enumerate(M[0]):
#             if item > 0.98:
#                 D3.add(index)
#         print D3
#         RList3 = []
#         for item in GList:
#             RList3.append(calculateR(item,D3))
#         print sum(RList3)/100.
#         A3R.append(sum(RList3)/100.)
#==============================================================================
        
    # Louvain Community Detection
    A4Result = community.best_partition(uncertainG,weight='prob')
    print "finish algorithm"
    A4Dict = {}
    for item in A4Result:
        if A4Result[item] not in A4Dict:
            A4Dict[A4Result[item]] = set([item])
        else:
            A4Dict[A4Result[item]].add(item)
    print "finish calculation"
    for start in testList:#uncertainG.nodes():
        RList4 = []
        D4 = A4Dict[A4Result[start]]
        for item in GList:
            RList4.append(calculateR(item,D4))
        A4R.append(sum(RList4)/100.)
    
#==============================================================================
#     # Girvan-Newman community detection algorithm
#     for (a,b) in uncertainG.edges():
#         uncertainG[a][b]['weight'] = 1.0 / (uncertainG[a][b]['prob']**0.3)
#     A5Dict = cmty.main(uncertainG)
#     A5Result = {}
#     for group in A5Dict:
#         for node in A5Dict[group]:
#             A5Result[node] = group
#     for start in uncertainG.nodes():
#         RList5 = []
#         D5 = A5Dict[A5Result[start]]
#         for item in GList:
#             RList5.append(calculateR(item,D5))
#         A5R.append(sum(RList5)/100.)
#==============================================================================
        
    #print A0R
    #print A1R
    print A2R
    #print A3R
    print A4R
    #print A5R
    print A6R
    print A7R
    print A8R
    print A9R
    print A10R
    print A11R
    #print sum(A0R)/len(A0R)
    #print sum(A1R)/len(A1R)
    print sum(A2R)/len(A2R)
    #print sum(A3R)/len(A3R)
    print sum(A4R)/len(A4R)
    #print sum(A5R)/len(A5R)
    print sum(A6R)/len(A6R)
    print sum(A7R)/len(A7R)
    print sum(A8R)/len(A8R)
    print sum(A9R)/len(A9R)
    print sum(A10R)/len(A10R)
    print sum(A11R)/len(A11R)
    return A1Dict, A4Dict, uncertainG
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
    DMax = D
    label = True
    R = 0
    RMax = R
    NotMaxCount = 0
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
                    save.tempB = dict(tempB) # v2版本这里没加dict
                    save.tempBIn = tempBIn
                    save.tempBTotal = tempBTotal
                    save.removeSet = set(removeSet) # v2版本这里没加set
                    tempSaveList.append(save)
            checkedNodeSet.add(node) # 循环结束，所有的sampleG都处理完了node，再把node添加上去
            changeRPrime = 0
            changeShareSNodeCount = 0
            for i in xrange(sampleNumber):
                changeRPrime += tempSaveList[i].RPrime
                changeShareSNodeCount += tempSaveList[i].shareSNodeCount
            changeRPrime = float(changeRPrime)/float(sampleNumber)
#==============================================================================
#             print ShareSNodeCount
#             print changeShareSNodeCount
#             print changeRPrime
#             print RPrime
#             print node
#==============================================================================
            if len(D) == 1 and changeRPrime!= 0:#changeRPrime可能是0，但ShareSNodeCount很大，原因是node和之前的node之间概率很小
                if changeShareSNodeCount > ShareSNodeCount or (changeShareSNodeCount == ShareSNodeCount and changeRPrime > RPrime):
                    saveList = tempSaveList
                    RPrime = changeRPrime
                    ShareSNodeCount = changeShareSNodeCount
            else:
                if changeRPrime > RPrime or (changeRPrime == RPrime and changeShareSNodeCount > ShareSNodeCount):
                    saveList = tempSaveList
                    RPrime = changeRPrime
                    ShareSNodeCount = changeShareSNodeCount
        if RPrime > RMax:
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
            DMax = set(D)
            RMax = R
            NotMaxCount = 0
        elif NotMaxCount < 1 and len(saveList) > 0: #见line421
            R = RPrime # 只是简单的复制粘贴，可能还有部分是多余的
            node = saveList[0].popNode #要是有个点是孤立的，这里会挂（saveList是空的）
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
            NotMaxCount += 1
        else:
            label = False
            
#==============================================================================
#     count = 0
#     for item in SGList:
#         print len(item.G.edges())
#         count += len(item.G.edges())
#     print float(count)/float(sampleNumber)
#==============================================================================
    return DMax, S, RMax, [item.G for item in SGList], [item.R for item in SGList], SGList
            
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
    
evaluationUncertainR()
#A1Dict, A4Dict, uncertainG = main()
#D, S, R, _, SGR, SGList, uncertainG, GList = main()