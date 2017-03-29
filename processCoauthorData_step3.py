#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 16:33:17 2017

@author: zhangchi
"""
import networkx as nx
import numpy as np

inputFile = open('coauthorData_multiAuthor_step2.txt','r')

G = nx.Graph()

for line in inputFile:
    line = line.strip().split(": ")
    time = int(line[0])
    authors = (line[1]+' ').split('//// ')[:-1]
    #print time
    if 20020101 <= time < 20050101:
        for i in range(len(authors)):
            for j in range(i+1,len(authors)):
                #print authors[i] + '/////' + authors[j]
                if G.has_edge(authors[i],authors[j]):
                    G[authors[i]][authors[j]]['count'] += 1
                else:
                    G.add_edge(authors[i],authors[j],count=1)
                    
for nodeA, nodeB in G.edges():
    G[nodeA][nodeB]['prob'] = 1 - np.exp(-0.5 * G[nodeA][nodeB]['count'])
    G[nodeA][nodeB]['weight'] = 1 / (G[nodeA][nodeB]['prob']**0.4)
'''
count = 0                    
for nodeA, nodeB in G.edges():
    if G[nodeA][nodeB]['count'] > 12:
        print nodeA + ' ' + nodeB + ' ' + str(G[nodeA][nodeB]['count'])
        count += 1
print count
'''