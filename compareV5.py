#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 16:52:33 2017

@author: zhangchi
"""

import networkx as nx
from ML_Handicapped_Paths import betweenness_centrality
import matplotlib.pyplot as plt
import numpy as np
from closeness import closeness_centrality
#from ML_Paths import betweenness_centrality
from matplotlib.ticker import MultipleLocator
import pickle

def changeWeight(G,r):
    for nodeA, nodeB in G.edges():
        G[nodeA][nodeB]['newWeight'] = G[nodeA][nodeB]['length'] / (G[nodeA][nodeB]['weight']**r)
    return G
    
def changeWeightlog(G):
    for nodeA, nodeB in G.edges():
        G[nodeA][nodeB]['newWeight'] = -np.log( G[nodeA][nodeB]['weight'])
    return G
    
def sampleGraph(G):
    newG = nx.Graph()
    for node in G.nodes():
        newG.add_node(node)
    for nodeA, nodeB in G.edges():
        probability = G[nodeA][nodeB]['weight']
        lengthValue = G[nodeA][nodeB]['length']
        if np.random.choice([1,0], p=[probability,1-probability]) == 1:
            newG.add_edge(nodeA, nodeB,length=lengthValue)
    return newG
    
def generateProbabilisticGraphOld(nodeNumber=100, edgeNumber=2000):
    # it also works
    G = nx.Graph()
    for i in range(nodeNumber):
        G.add_node(i)
    for _ in range(edgeNumber):
        nodeA = np.random.randint(nodeNumber)
        nodeB = np.random.randint(nodeNumber)
        while G.has_edge(nodeA,nodeB):
            nodeA = np.random.randint(nodeNumber)
            nodeB = np.random.randint(nodeNumber)
        G.add_edge(nodeA,nodeB,weight=-np.random.uniform()+1,length=np.random.uniform(1,3))
    return G
    
def generateProbabilisticGraph():    
    G = nx.random_partition_graph([30,50,120],0.2,0.02)
    for nodeA, nodeB in G.edges():
        G[nodeA][nodeB]['weight'] = -np.random.uniform()+1
        #G[nodeA][nodeB]['length'] = np.random.uniform(1,3)
        G[nodeA][nodeB]['length'] = 1
    return G

gamaRange = [0.01,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.7,0.8]
dictionary = {}
for gama in gamaRange:
    dictionary[gama] = []
#G = generateProbabilisticGraphOld()
for index in range(20):
    print index
    G = generateProbabilisticGraph()
    
    result = None
    for i in range(100):
        #print i
        newG = sampleGraph(G)
        z = nx.betweenness_centrality(newG,weight='length')
        #z = nx.closeness_centrality(newG,distance ='length')
        sorted_z = {key: rank for rank, key in enumerate(sorted(z, key=z.get, reverse=True), 1)}
        #sorted_z = z
        if result is None:
            result = sorted_z
        else:
            for item in result:
                result[item] = result[item] + sorted_z[item]
    sorted_z = {key: rank for rank, key in enumerate(sorted(result, key=result.get, reverse=False), 1)}
    
    #==============================================================================
    # following: experiment 2
    #==============================================================================
    differenceExperimentHistory = []
    for r in gamaRange:
        G = changeWeight(G,r)
        b = nx.betweenness_centrality(G,weight = 'newWeight')
        #b = nx.closeness_centrality(G,distance = 'newWeight')
        sorted_b = {key: rank for rank, key in enumerate(sorted(b, key=b.get, reverse=True), 1)}
        
        differenceExperiment = 0
        for key in sorted_b:
            if key in sorted_z:
                #plt.scatter(sorted_z[key], sorted_b[key],color = 'Red')
                differenceExperiment = differenceExperiment + abs(sorted_z[key] - sorted_b[key])
        #plt.plot([0,160],[0,160], color ='Blue', linewidth=3.5, linestyle="--")
        #plt.title('Simulation: Betweenness Centrality on unweighted graph')
        #plt.title('Simulation: Closeness Centrality on unweighted graph')
        #plt.title('Simulation: Betweenness Centrality on weighted graph')
        #plt.title('Simulation: Closeness Centrality on weighted graph')
        #plt.xlabel('Sample Rankings')
        #plt.ylabel('-log(probability) Rankings, r = '+ str(r))
        #plt.show()
        print differenceExperiment
        differenceExperimentHistory.append(differenceExperiment)
        dictionary[r].append(differenceExperiment)
    
    plt.plot(gamaRange, differenceExperimentHistory)
    plt.xlabel('Lambda Value')
    plt.ylabel('Linearity')
    plt.show()

finalResult = []
for item in gamaRange:
    finalResult.append(np.average(dictionary[item])*1.0/((2**0.5)*200))  
fig = plt.figure()
fig.set_size_inches(8,5.5)
plt.xlim(-0.05,0.85)
xmajorLocator = MultipleLocator(0.1)
xminorLocator = MultipleLocator(0.05)
ymajorLocator = MultipleLocator(2) #将y轴主刻度标签设置为0.5的倍数
yminorLocator = MultipleLocator(1)
ax = fig.add_subplot(111)
ax.xaxis.set_major_locator(xmajorLocator)
ax.xaxis.set_minor_locator(xminorLocator)
ax.yaxis.set_major_locator(ymajorLocator)
ax.yaxis.set_minor_locator(yminorLocator)
# http://blog.sina.com.cn/s/blog_a7ace3d80102wbhs.html
#==============================================================================
# for i,j in zip(gamaRange,finalResult):
#     ax.annotate('%s)' %j, xy=(i,j), xytext=(30,0), textcoords='offset points')
#     ax.annotate('(%s,' %i, xy=(i,j))
#==============================================================================
plt.plot(gamaRange,finalResult,linewidth=2.5)
plt.xlabel('Lambda Value')
plt.ylabel('Average Linear Correlation')
#plt.title('Parameter Setting for Betweenness Centrality on Unweighted Graph')
#plt.title('Parameter Setting for Closeness Centrality on Unweighted Graph')
#plt.title('Parameter Setting for Betweenness Centrality on Weighted Graph')
#plt.title('Parameter Setting for Closeness Centrality on Weighted Graph')
ax.xaxis.grid(True, which='major') #x坐标轴的网格使用主刻度
ax.yaxis.grid(True, which='minor') #y坐标轴的网格使用次刻度
plt.show()
#pickle.dump( [dictionary], open( "BCW.p", "wb" ) )
#pickle.dump( [dictionary], open( "CCW.p", "wb" ) )
pickle.dump( [dictionary], open( "BCU.p", "wb" ) )
#pickle.dump( [dictionary], open( "CCU.p", "wb" ) )