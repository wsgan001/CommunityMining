#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 21:07:07 2017

@author: zhangchi
"""

import numpy as np

def generateAllPossibility(length):
    candidate = [0] * length
    count = 0
    total = 2 ** length
    while count < total:
        yield candidate # first time using yield
        count += 1
        temp = 1
        index = 0
        while temp == 1 and index < length:
            if candidate[index] == 0:
                candidate[index] = 1
                temp = 0
            else:
                candidate[index] = 0
                temp = 1
                index += 1
                
def calculate(G,neighborList):
    length = len(neighborList)
    connected = 0
    disconnected = 0
    for i in xrange(length-1):
        for j in xrange(i+1,length):
            if G.has_edge(neighborList[i],neighborList[j]):
                prob = G.edge[neighborList[i]][neighborList[j]]['prob']
                connected += prob
                disconnected += (1-prob)
            else:
                disconnected += 1
    return float(connected+1)/float(disconnected+1)

def sampleGraphAndCalculate(G, node):
    neighborList = []
    for n in G[node]:
        probability = G.edge[node][n]['prob']
        if np.random.choice([1,0], p=[probability,1-probability]) == 1:
            neighborList.append(n)
    return calculate(G,neighborList)

def sampleBasedLNBCalculation(G, node):
    neighborList = G[node].keys()
    length = len(neighborList)
    if length <= 6:
        value = 0
        for possibility in generateAllPossibility(length):
            probability = 1
            neighbors = []
            for exist, n in zip(possibility, neighborList):
                if exist == 1:
                    probability *= G.edge[node][n]['prob']
                    neighbors.append(n)
                else:
                    probability *= (1 - G.edge[node][n]['prob'])
            value += probability * calculate(G,neighbors)
        return value
    else:
        value = 0
        sampleNumber = 50
        size = 1./float(sampleNumber)
        for _ in xrange(sampleNumber):
            value += size * sampleGraphAndCalculate(G,node)
        return value
                
        