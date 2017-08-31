#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 22:55:53 2017

@author: zhangchi
"""

# node2vec + logistic regression

import networkx as nx
import numpy as np
import random
from sklearn import linear_model
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from numpy import linalg as LA

def function(index, uVec, vVec):
    if index == 0:
        return np.multiply(uVec,vVec)
    elif index == 1:
        return np.concatenate((uVec,vVec))

# generate input file for node2vec

def generateInputFileForNode2vec():
    G = nx.Graph()
    File = open("USAir.txt","r") # 0.1, 0.2, 0.3这附近比较好
    for line in File:
        lineList = line.strip().split("    ")
        nodeA = int(lineList[0])
        nodeB = int(lineList[1])
        G.add_edge(nodeA,nodeB)
        
    edgeTrain, edgeTest = train_test_split(G.edges(), test_size=0.1)
            
    newG = nx.Graph()
    for nodeA, nodeB in edgeTrain:
        newG.add_edge(nodeA,nodeB)
        
    nodeList = newG.nodes()
    nodeList.sort()
    for node in nodeList:
        print str(node) + " " + " ".join([str(item) for item in newG[node]])
    return G, newG
        
def generateDictionary():
    File = open("usAir.embeddings","r")
    dic = {}
    for line in File:
        lineList = line.strip().split(" ")
        if len(lineList) > 5:
            temp = []
            for i in xrange(1,len(lineList)):
                temp.append(float(lineList[i]))
            dic[int(lineList[0])] = np.array(temp)
    return dic

def generateTrainData(G, dic):
    X = []
    Y = []
    edgeNumber = len(G.edges()) * 100
    for u, v in G.edges():
        uVec = dic[u]
        vVec = dic[v]
        X.append(function(1,uVec,vVec))
        Y.append(1)
        #Y.append([0,1])
    nonEdge = list(nx.non_edges(G))
    random.shuffle(nonEdge)
    count = 0
    for u, v in nonEdge:
        if count < edgeNumber:
            count += 1
            uVec = dic[u]
            vVec = dic[v]
            X.append(function(1,uVec,vVec))
            Y.append(0)
            #Y.append([1,0])
        else:
            break
    return X, Y

def trainModel(trainX, trainY):
# =============================================================================
#     regr = linear_model.LinearRegression()
#     model = regr.fit(trainX, trainY)
#     return model
# =============================================================================
    clf = SVC(probability=True)
    clf.fit(trainX, trainY) 
    return clf

def node2vecLRPredict(G, model, dic):
    preds = []
    for u, v in nx.non_edges(G):
        if len(list(nx.common_neighbors(G, u, v))) > 0:
            uVec = dic[u]
            vVec = dic[v]
            #result = model.predict([function(1,uVec,vVec)])
            result = model.predict_proba([function(1,uVec,vVec)])
            
# =============================================================================
#             score = 0
#             for node in nx.common_neighbors(G, u, v):
#                 #score += 1.
#                 #score += 1. / np.log10(len(G[node]))
#                 score += 1. / float(len(G[node]))
#                 
# =============================================================================
            #preds.append([u,v,result])
            preds.append([u,v,float(result[0][1])/float(result[0][0])])
    return preds

def common_neighbor(G,dic):
    averageDis = averageDistance(G,dic)
    def predict(u, v):
        result = 0
        for node in nx.common_neighbors(G, u, v):
            #result += 1. * distance(dic[node],dic[u],dic[v])
            #result += (1. * distance(dic[node],dic[u],dic[v])) / (np.log10(len(G[node])) *  averageDis)
            result += (1. ) / (float(len(G[node])))
        return result
    return ((u, v, predict(u, v)) for u, v in nx.non_edges(G))

def distance(a,b,c):
    aAndb = LA.norm(a-b, 1)
    aAndc = LA.norm(a-c, 1)
    return aAndb+aAndc
    #return max(aAndb,aAndc)

def averageDistance(G, dic):
    dis = 0
    count = 0
    nodeList = G.nodes()
    for i in xrange(len(nodeList)):
        for j in xrange(i+1,len(nodeList)):
            count += 1
            dis += LA.norm(dic[nodeList[i]]-dic[nodeList[j]], 1)
    return float(dis)/float(count)
            

#G, newG = generateInputFileForNode2vec()

dic = generateDictionary()
X, Y = generateTrainData(newG, dic)
print "start training"
model = trainModel(X, Y)
print "finish training"
result = node2vecLRPredict(newG,model,dic)
print "finish predicting"
accuracyList = []
result.sort(key=lambda x:x[2],reverse=True)
right = 0
for nodeA, nodeB, score in result[:100]:
    if G.has_edge(nodeA,nodeB):
        right += 1
accuracyList.append(float(right)/100.)
    
# =============================================================================
# dic = generateDictionary()
# preds = common_neighbor(newG,dic)
# result = []
# for u, v, p in preds:
#     result.append([u,v,p])
# print "finish predicting"
# accuracyList = []
# result.sort(key=lambda x:x[2],reverse=True)
# right = 0
# for nodeA, nodeB, score in result[:100]:
#     if G.has_edge(nodeA,nodeB):
#         right += 1
# accuracyList.append(float(right)/100.)
# =============================================================================
        
# generateInputFileForNode2vec()