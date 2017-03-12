#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 19:32:33 2017

@author: zhangchi
"""


import networkx as nx
import numpy as np
import operator
import matplotlib.pyplot as plt 

def readNet(input_file, now, sep_char=' '): 
    num_lines = 0
    G = nx.DiGraph()
    for line in open(input_file):
        num_lines += 1
        line = line.rstrip().split(sep_char)
        if line[1] == line[2]:
            pass
        elif int(line[0]) <= now:
            if G.has_edge(line[1], line[2]) is False:            
                G.add_edge(line[1], line[2], time = [int(line[0])])
            else:
                G[line[1]][line[2]]['time'].append(int(line[0]))
        else:
            break
    return G

def getWeight(timeList, now):
    possibility = 1
    for time in timeList:
        if time <= now:
            possibility = possibility * (1 - np.exp((time-now)/2419200.))
        else:
            break
    linkPossibility = 1 - possibility
    return linkPossibility
        
def updateWeight(G, now):
    for nodeA, nodeB in G.edges():
        timeList = G[nodeA][nodeB]['time']
        G[nodeA][nodeB]['weight'] = getWeight(timeList,now)
    return G

def findRank(sorted_x, number):
    length = len(sorted_x)
    count = 0
    for item in sorted_x:
        count = count + 1
        if item[0] == number:
            #return length-count
            return int(151.*(length-count)/length)
    #return length
    return 151

result = []
for i in range(80):
    G=readNet('resultFullData.txt',927590400+1209600*i)
    #nx.draw(G)
    G = updateWeight(G, 927590400+1209600*i)
    try:
        x = nx.pagerank(G,alpha=1,max_iter=500)
        #x = closeness_centrality(G)
        sorted_x = sorted(x.items(), key=operator.itemgetter(1))
        #tempResult = findRank(sorted_x,'kenneth.lay@enron.com')
        #tempResult = findRank(sorted_x,'jeff.skilling@enron.com')
        tempResult = findRank(sorted_x,'lavorato@enron.com')
        print str(i) + ': ' + str(tempResult)
        result.append(151-tempResult)
    except:
        pass

plt.figure(0)
plt.axis([0, 80, 0, 155])    
plt.plot(result)
plt.show()

'''

G = nx.DiGraph()
G.add_edge(1,2,weight=0.25)
G.add_edge(1,3,weight=0.5)
G.add_edge(1,4,weight=0.5)
G.add_edge(2,1,weight=1)
G.add_edge(2,4,weight=1)
G.add_edge(3,1,weight=1)
G.add_edge(4,2,weight=1)
G.add_edge(4,3,weight=1)
centrality = nx.pagerank(G,alpha=1)
print centrality

import numpy as np
a = np.array([[0,0.5,1,0],[0.2,0,0,0.5],[0.4,0,0,0.5],[0.4,0.5,0,0]])
b=np.array([[0.25],[0.25],[0.25],[0.25]])
for _ in range(200):
    b = a.dot(b)
'''