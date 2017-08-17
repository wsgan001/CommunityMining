#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 18:25:59 2017

@author: zhangchi
"""

# start link prediction

import networkx as nx
import numpy as np
from sklearn.model_selection import train_test_split

def common_neighbor(G):
    def predict(u, v):
        result = 0
        for node in nx.common_neighbors(G, u, v):
            result += 1.
            #result += 1. / np.log10(len(G[node]))
            #result += 1. / float(len(G[node]))
        return result
    return ((u, v, predict(u, v)) for u, v in nx.non_edges(G))

def LNB(G):
    nodeNumber = len(G.nodes())
    M = nodeNumber * (nodeNumber - 1) / 2
    MT = len(G.edges())
    s = float(M)/float(MT) - 1
    dic = {}
    for node in G.nodes():
        neighborList = G[node].keys()
        length = len(neighborList)
        connected = 0
        disconnected = 0
        for i in xrange(length-1):
            for j in xrange(i+1,length):
                if G.has_edge(neighborList[i],neighborList[j]):
                    connected += 1
                else:
                    disconnected += 1
        dic[node] = float(connected+1)/float(disconnected+1)
    def predict(u, v):
        result = 0
        for node in nx.common_neighbors(G, u, v):
            result += np.log10(s) + np.log10(dic[node])
            #result += (np.log10(s) + np.log10(dic[node])) / np.log10(len(G[node]))
            #result += (np.log10(s) + np.log10(dic[node])) / len(G[node])
        return result
    return ((u, v, predict(u, v)) for u, v in nx.non_edges(G))

def LNBVersion2(G):
    # 已知两个节点相连，那么这两个节点的共同邻居包含w的概率是多少
    PWA1 = {}
    PWA2 = {}
    for node in G.nodes():
        PWA1[node] = 0
        PWA2[node] = 0
    for n1, n2 in G.edges():
        n1Neighbor = set(G[n1].keys())
        n2Neighbor = set(G[n2].keys())
        intersection = n1Neighbor.intersection(n2Neighbor)
        for node in intersection:
            PWA1[node] += 1
    existEdgeNumber = len(G.edges())
    
    for n1, n2 in nx.non_edges(G):
        n1Neighbor = set(G[n1].keys())
        n2Neighbor = set(G[n2].keys())
        intersection = n1Neighbor.intersection(n2Neighbor)
        for node in intersection:
            PWA2[node] += 1
    nonexistEdgeNumber = len(list(nx.non_edges(G)))
    
    for node in G.nodes():
        PWA1[node] = float(PWA1[node]+1)/float(existEdgeNumber-PWA1[node]+1)
        PWA2[node] = float(PWA2[node]+1)/float(nonexistEdgeNumber-PWA2[node]+1)
    
    def predict(u, v):
        result = 0
        for node in nx.common_neighbors(G, u, v):
            #result += np.log10(PWA1[node]/PWA2[node])
            result += np.log10(PWA1[node]/PWA2[node]) / np.log10(len(G[node]))
            #result += np.log10(PWA1[node]/PWA2[node]) / len(G[node])
        return result
    return ((u, v, predict(u, v)) for u, v in nx.non_edges(G))

def main():
    G = nx.Graph()
    File = open("USAir.txt","r")
    for line in File:
        lineList = line.strip().split("    ")
        nodeA = int(lineList[0])
        nodeB = int(lineList[1])
        G.add_edge(nodeA,nodeB)
    
    accuracyList = []
    for count in xrange(100):
        print count
        edgeTrain, edgeTest = train_test_split(G.edges(), test_size=0.1)
        
        newG = nx.Graph()
        for nodeA, nodeB in edgeTrain:
            newG.add_edge(nodeA,nodeB)
        #preds = common_neighbor(newG)
        #preds = LNB(newG)
        preds = LNBVersion2(newG)
        #preds = nx.adamic_adar_index(newG)
        #preds = nx.jaccard_coefficient(newG)
        
        result = []
        for u, v, p in preds:
            result.append([u,v,p])
        result.sort(key=lambda x:x[2],reverse=True)
        right = 0
        for nodeA, nodeB, score in result[:100]:
            if G.has_edge(nodeA,nodeB):
                right += 1
        accuracyList.append(float(right)/100.)
        
    print accuracyList    
    print sum(accuracyList)/100.
    
main()


