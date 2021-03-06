#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 11:56:04 2017

@author: zhangchi
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from dijkstra_prob import single_source_dijkstra_path_length
import pickle

TIME1 = 20040101
TIME2 = 20050101
TIME3 = 20060101

def exp_range(start, end, mul):
    while start < end:
        yield start
        start *= mul

inputFile = open('coauthorData_multiAuthor_step2.txt','r')

G = nx.Graph()

for line in inputFile:
    line = line.strip().split(": ")
    time = int(line[0])
    authors = (line[1]+' ').split('//// ')[:-1]
    #print time
    if TIME1 <= time < TIME2:
        for i in range(len(authors)):
            #authorList.append(authors[i])
            for j in range(i+1,len(authors)):
                #print authors[i] + '/////' + authors[j]
                if G.has_edge(authors[i],authors[j]):
                    G[authors[i]][authors[j]]['count'] += 1
                else:
                    G.add_edge(authors[i],authors[j],count=1)
    
authorList = sorted(nx.connected_components(G), key = len, reverse=True)[0]
print(len(authorList))
G = nx.Graph()
newG = nx.Graph()

inputFile = open('coauthorData_multiAuthor_step2.txt','r')
                    
for line in inputFile:
    line = line.strip().split(": ")
    time = int(line[0])
    authors = (line[1]+' ').split('//// ')[:-1]
    #print time
    if 20010101 < time < TIME2:
        newAuthors = []
        for author in authors:
            if author in authorList:
                newAuthors.append(author)
        authors = newAuthors
        for i in range(len(authors)):
            for j in range(i+1,len(authors)):
                #print authors[i] + '/////' + authors[j]
                if G.has_edge(authors[i],authors[j]):
                    G[authors[i]][authors[j]]['count'] += 1
                else:
                    G.add_edge(authors[i],authors[j],count=1)
    elif TIME2 <= time < 20100101:
        newAuthors = []
        for author in authors:
            if author in authorList:
                newAuthors.append(author)
        for i in range(len(newAuthors)):
            for j in range(i+1,len(newAuthors)):
                if (newAuthors[i],newAuthors[j]) not in G.edges() and (newAuthors[j],newAuthors[i]) not in G.edges():
                    newG.add_edge(newAuthors[i],newAuthors[j])

tempList = []
for sz in exp_range(1, 90, 1.2):
    if int(sz) not in tempList:
        tempList.append(int(sz))
#tempList = tempList[:10]
tempList += range(90,len(G.nodes())-1,30)
#tempList.append(len(G.nodes())-1)
                
print 'finish step 1'
                    
for nodeA, nodeB in G.edges():
    G[nodeA][nodeB]['prob'] = 1 - np.exp(-0.5 * G[nodeA][nodeB]['count'])
    G[nodeA][nodeB]['weight'] = 1 / (G[nodeA][nodeB]['prob']**0.4)
    G[nodeA][nodeB]['logweight'] = -np.log(G[nodeA][nodeB]['prob'])

dictionaryWeight = {}
dictionaryWeightRank = {}
dictionaryProb = {}
dictionaryProbRank = {}
dictionaryLogWeight = {}
dictionaryLogWeightRank = {}

nodeCount = 0
for node in G.nodes():
    nodeCount += 1
    if nodeCount % 1000 == 0:
        print nodeCount
        
    distance = single_source_dijkstra_path_length(G,node,beta=1,weight='prob')
    topKList = sorted(distance,key=distance.get,reverse=True)[1:]
    dictionaryProb[node] = distance
    dictionaryProbRank[node] = topKList
print nodeCount
    
#pickle.dump([dictionaryProb,dictionaryProbRank],open( "/Volumes/My Passport 1/prob.p", "wb" )) 

nodeNumber = len(G.nodes())
    
nodeCount = 0
falsePositiveRateHistory = [0]
truePositiveRateHistory = [0]
for k in tempList:
    print k
    TPList = []
    FPList = []
    conditionPositiveList = []
    conditionNegativeList = []
    for node in G.nodes():
        nodeCount += 1
        #distance = single_source_dijkstra_path_length(G,node,cutoff=0.0073,weight='prob')
        #topKList = sorted(distance,key=distance.get,reverse=True)[1:]
        topKList = dictionaryProbRank[node][:k]
        if newG.has_node(node):
            groundTruth = newG[node].keys()
        else:
            groundTruth = []
        groundTruthLength = len(groundTruth)
        count = 0
        for item in groundTruth:
            if item in topKList:
                count += 1
        TPList.append(count)
        FPList.append(len(topKList) - count)
        conditionPositiveList.append(groundTruthLength)
        conditionNegativeList.append(nodeNumber - 1 - groundTruthLength)
    # ------ #
    truePositiveRate = np.sum(TPList) * 1.0 / np.sum(conditionPositiveList)
    falsePositiveRate = np.sum(FPList) * 1.0 / np.sum(conditionNegativeList)
    print str(falsePositiveRate) + '  '+ str(truePositiveRate)
    falsePositiveRateHistory.append(falsePositiveRate)
    truePositiveRateHistory.append(truePositiveRate)
plt.plot(falsePositiveRateHistory, truePositiveRateHistory,label='Most Probable Path',color="red")

#del dictionaryProb
#del dictionaryProbRank

#==============================================================================
# cutoff=5 vs cutoff=0.0073 is almost tie
# 0.00267103968079  0.715554862843
# 0.00267621045755  0.715554862843
#==============================================================================

nodeCount = 0
for node in G.nodes():
    nodeCount += 1
    if nodeCount % 1000 == 0:
        print nodeCount
        
    distance = nx.single_source_dijkstra_path_length(G,node,weight='weight')
    topKList = sorted(distance,key=distance.get)[1:]
    dictionaryWeight[node] = distance
    dictionaryWeightRank[node] = topKList
print nodeCount

#pickle.dump([dictionaryWeight,dictionaryWeightRank],open( "/Volumes/My Passport 1/weight.p", "wb" ))

nodeNumber = len(G.nodes())
    
nodeCount = 0
falsePositiveRateHistory = [0]
truePositiveRateHistory = [0]
for k in tempList:
    print k
    TPList = []
    FPList = []
    conditionPositiveList = []
    conditionNegativeList = []
    for node in G.nodes():
        nodeCount += 1
        #distance = nx.single_source_dijkstra_path_length(G,node,cutoff=5,weight='weight')
        #topKList = sorted(distance,key=distance.get)[1:]
        topKList = dictionaryWeightRank[node][:k]
        if newG.has_node(node):
            groundTruth = newG[node].keys()
        else:
            groundTruth = []
        groundTruthLength = len(groundTruth)
        count = 0
        for item in groundTruth:
            if item in topKList:
                count += 1
        TPList.append(count)
        FPList.append(len(topKList) - count)
        conditionPositiveList.append(groundTruthLength)
        conditionNegativeList.append(nodeNumber - 1 - groundTruthLength)
    # ------ #
    truePositiveRate = np.sum(TPList) * 1.0 / np.sum(conditionPositiveList)
    falsePositiveRate = np.sum(FPList) * 1.0 / np.sum(conditionNegativeList)
    print str(falsePositiveRate) + '  '+ str(truePositiveRate)
    falsePositiveRateHistory.append(falsePositiveRate)
    truePositiveRateHistory.append(truePositiveRate)
plt.plot(falsePositiveRateHistory, truePositiveRateHistory,label='Inversed Probabilistic Graph',color="blue")  

#del dictionaryWeight
#del dictionaryWeightRank

#==============================================================================
# algorithm 3
#==============================================================================

nodeCount = 0
for node in G.nodes():
    nodeCount += 1
    if nodeCount % 1000 == 0:
        print nodeCount
        
    distance = nx.single_source_dijkstra_path_length(G,node,weight='logweight')
    topKList = sorted(distance,key=distance.get)[1:]
    dictionaryLogWeight[node] = distance
    dictionaryLogWeightRank[node] = topKList
print nodeCount

#pickle.dump([dictionaryWeight,dictionaryWeightRank],open( "/Volumes/My Passport 1/weight.p", "wb" ))

nodeNumber = len(G.nodes())
    
nodeCount = 0
falsePositiveRateHistory = [0]
truePositiveRateHistory = [0]
for k in tempList:
    print k
    TPList = []
    FPList = []
    conditionPositiveList = []
    conditionNegativeList = []
    for node in G.nodes():
        nodeCount += 1
        #distance = nx.single_source_dijkstra_path_length(G,node,cutoff=5,weight='weight')
        #topKList = sorted(distance,key=distance.get)[1:]
        topKList = dictionaryLogWeightRank[node][:k]
        if newG.has_node(node):
            groundTruth = newG[node].keys()
        else:
            groundTruth = []
        groundTruthLength = len(groundTruth)
        count = 0
        for item in groundTruth:
            if item in topKList:
                count += 1
        TPList.append(count)
        FPList.append(len(topKList) - count)
        conditionPositiveList.append(groundTruthLength)
        conditionNegativeList.append(nodeNumber - 1 - groundTruthLength)
    # ------ #
    truePositiveRate = np.sum(TPList) * 1.0 / np.sum(conditionPositiveList)
    falsePositiveRate = np.sum(FPList) * 1.0 / np.sum(conditionNegativeList)
    print str(falsePositiveRate) + '  '+ str(truePositiveRate)
    falsePositiveRateHistory.append(falsePositiveRate)
    truePositiveRateHistory.append(truePositiveRate)
plt.plot(falsePositiveRateHistory, truePositiveRateHistory,label='Negative Logarithm',color="black")  

#del dictionaryLogWeight
#del dictionaryLogWeightRank


plt.title('DBLP: Link prediction')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend(loc=4)
plt.grid()
plt.show()