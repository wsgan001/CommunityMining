#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 00:30:39 2017

@author: zhangchi
"""

import networkx as nx
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn import linear_model

dic = {}

def generateTrainData(G):
    X = []
    Y = []
    for u, v in G.edges():
        sampleX = [0] * len(G.nodes())
        for node in nx.common_neighbors(G, u, v):
            sampleX[dic[node]] = G.edge[node][u]['prob'] * G.edge[node][v]['prob']
        X.append(sampleX)
        Y.append(G.edge[u][v]['prob'])
    return X, Y

def predict(G, model):
    preds = []
    for u, v in nx.non_edges(G):
        if len(list(nx.common_neighbors(G, u, v))) > 0:
            sampleX = [0] * len(G.nodes())
            for node in nx.common_neighbors(G, u, v):
                sampleX[dic[node]] = G.edge[node][u]['prob'] * G.edge[node][v]['prob']
            result = model.predict([sampleX])
            preds.append([u,v,result])
    return preds

def addProb(G,prob=0.9,percent=0.15):
    for a,b in G.edges():
        value = 0.5 * np.random.randn() + prob
        while value <= 0 or value > 1:
            value = 0.5 * np.random.randn() + prob
        G.edge[a][b]['prob'] = value
        #G.edge[a][b]['weight'] = 1
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
    
        G.add_edge(nodeA,nodeB,prob=value)#,weight=1)
        count += 1
    return G

# =============================================================================
# G = nx.Graph()
# File = open("USAir.txt","r")
# for line in File:
#     lineList = line.strip().split("    ")
#     nodeA = int(lineList[0])
#     nodeB = int(lineList[1])
#     G.add_edge(nodeA,nodeB)
# =============================================================================

G = nx.Graph()
File = open("/Users/zhangchi/Desktop/cs690/CommunityMining/community-detection/TAP_core.txt")
for line in File:
    edgeList = line.strip().split('\t')
    G.add_edge(edgeList[0],edgeList[1],prob=float(edgeList[2]))
    
for index, item in enumerate(G.nodes()):
    dic[item] = index

accuracyList = []
for count in xrange(1):
    print count
    edgeTrain, edgeTest = train_test_split(G.edges(), test_size=0.1)
    
    newG = nx.Graph()
    for node in G.nodes():
        newG.add_node(node)
    for nodeA, nodeB in edgeTrain:
        #newG.add_edge(nodeA,nodeB)
        newG.add_edge(nodeA,nodeB,prob=G.edge[nodeA][nodeB]['prob'])
    #newG = addProb(newG,prob=0.8,percent=0.4)
    
    trainX, trainY = generateTrainData(newG)
    svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
    #svr_lin = SVR(kernel='linear', C=1e3)
    #svr_poly = SVR(kernel='poly', C=1e3, degree=2)
    #regr = linear_model.LinearRegression()
    model = svr_rbf.fit(trainX, trainY)
    #model = svr_lin.fit(trainX, trainY)
    #model = svr_poly.fit(trainX, trainY)
    #regr.fit(trainX, trainY)
    #model = regr
    print "finish training"
    result = predict(newG,model)
    print "finish predicting"

    result.sort(key=lambda x:x[2],reverse=True)
    right = 0
    for nodeA, nodeB, score in result[:100]:
        if G.has_edge(nodeA,nodeB):
            right += 1
    accuracyList.append(float(right)/100.)
    
print accuracyList
print sum(accuracyList)/1.