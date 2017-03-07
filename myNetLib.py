#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 00:51:53 2017

@author: zhangchi
"""

 
import networkx as nx
#import numpy as np
import matplotlib.pyplot as plt 
#import random
import operator

# Routine for reading in a network as an edge list.
def readnet(input_file , time, sep_char=' ' , comment_char='#'): 
    num_lines = 0
    G = nx.Graph()
    for line in open(input_file):
        num_lines += 1
        if line[0] != comment_char:
            line = line.rstrip().split(sep_char) 
            if len(line) == 3:
                if int(line[0]) < time:
                    G.add_edge(int(line[1]), int(line[2])) 
                    #if num_lines < 10:
                        #print line[0] + " " + line[1] 
                    #if num_lines == 10:
                        #print "..."
                else:
                    break
    #print 'Read ' + str(num_lines) + ' lines.'
    #print 'Network has %d nodes and %d edges.' % (G.number_of_nodes(), G.number_of_edges())
    return G

def findRank(sorted_x, number):
    length = len(sorted_x)
    count = 0
    for item in sorted_x:
        count = count + 1
        if item[0] == number:
            return int(184.*(length-count)/length)
    return 184
#G=readnet('enronData.txt')

for j in range(184):
    result = []
    for i in range(84):
        G=readnet('result.txt',926380800+1209600*i)
        #nx.draw(G)
        x = nx.betweenness_centrality(G)
        sorted_x = sorted(x.items(), key=operator.itemgetter(1))
        tempResult = findRank(sorted_x,67)
        #print tempResult
        result.append(184-tempResult)
    print j
    plt.figure(j)
    plt.axis([0, 85, 0, 190])    
    plt.plot(result)
    plt.show()
'''
print G[1]
print len(G[1])
'''


'''
# check result
a=open('enronData.txt')
result = []
for line in a:
    if int(line.split()[0]) == 1:
        if line.split()[1] not in result:
            result.append(line.split()[1])
    if int(line.split()[1]) == 1:
        if line.split()[0] not in result:
            result.append(line.split()[1])


import pandas as pd
import numpy as np
inputFile = pd.read_csv("FinalAdjacencyMatrix.csv").drop(['name'],axis=1)
inputFileNumpy = np.array(inputFile.as_matrix(),dtype=np.int)
for i in range(30):
    print np.sum(inputFileNumpy[:,i])+np.sum(inputFileNumpy[i,1:])
'''
    
