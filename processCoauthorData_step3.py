#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 16:33:17 2017

@author: zhangchi
"""
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

inputFile = open('coauthorData_multiAuthor_step2.txt','r')

G = nx.Graph()
newG = nx.Graph()
authorList = []

for line in inputFile:
    line = line.strip().split(": ")
    time = int(line[0])
    authors = (line[1]+' ').split('//// ')[:-1]
    #print time
    if 20020101 <= time < 20050101:
        for i in range(len(authors)):
            authorList.append(authors[i])
            for j in range(i+1,len(authors)):
                #print authors[i] + '/////' + authors[j]
                if G.has_edge(authors[i],authors[j]):
                    G[authors[i]][authors[j]]['count'] += 1
                else:
                    G.add_edge(authors[i],authors[j],count=1)
    elif 20050101 <= time < 20060101:
        newAuthors = []
        for author in authors:
            if author in authorList:
                newAuthors.append(author)
        for i in range(len(newAuthors)):
            for j in range(i+1,len(newAuthors)):
                newG.add_edge(newAuthors[i],newAuthors[j])
                    
for nodeA, nodeB in G.edges():
    G[nodeA][nodeB]['prob'] = 1 - np.exp(-0.5 * G[nodeA][nodeB]['count'])
    G[nodeA][nodeB]['weight'] = 1 / (G[nodeA][nodeB]['prob']**0.4)
    
nodeNumber = len(G.nodes())
    
falsePositiveRateList = []
truePositiveRateList = []
nodeCount = 0
for node in G.nodes():
    nodeCount += 1
    if nodeCount % 1000 == 0:
        print nodeCount
    if newG.has_node(node):
        distance = nx.single_source_dijkstra_path_length(G,node,cutoff=5,weight='weight')
        topKList = sorted(distance,key=distance.get)[1:]
        groundTruth = newG[node].keys()
        groundTruthLength = len(groundTruth)
        count = 0
        for item in groundTruth:
            if item in topKList:
                count += 1
        falsePositiveRateTemp = (len(topKList) - count) * 1.0 / (nodeNumber - groundTruthLength)
        truePositiveRateTemp = count * 1.0 / groundTruthLength
        falsePositiveRateList.append(falsePositiveRateTemp)
        truePositiveRateList.append(truePositiveRateTemp)
# ------ #
falsePositiveRate = np.average(falsePositiveRateList)
truePositiveRate = np.average(truePositiveRateList)
print str(falsePositiveRate) + '  '+ str(truePositiveRate)
plt.scatter(falsePositiveRate, truePositiveRate)    
    
    
'''
count = 0                    
for nodeA, nodeB in G.edges():
    if G[nodeA][nodeB]['count'] > 12:
        print nodeA + ' ' + nodeB + ' ' + str(G[nodeA][nodeB]['count'])
        count += 1
print count
'''