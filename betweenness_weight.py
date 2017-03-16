#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 15:40:59 2017

@author: zhangchi
"""

import networkx as nx
import numpy as np
import operator
import matplotlib.pyplot as plt 
#from ML_Paths import betweenness_centrality
#from ML_Handicapped_Paths import betweenness_centrality
#from closeness import closeness_centrality
'''
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
'''
def readNet(input_file, now, sep_char=' '): 
    num_lines = 0
    G = nx.Graph()
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
            #possibility = possibility * (1 - np.exp((time-now)/2419200.))
            possibility = possibility * (1 - np.exp((time-now)/63244800.))
        else:
            break
    linkPossibility = 1 - possibility
    return linkPossibility
        
def updateWeight(G, now):
    for nodeA, nodeB in G.edges():
        timeList = G[nodeA][nodeB]['time']
        G[nodeA][nodeB]['weight'] = 1.0 / getWeight(timeList,now)
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
    
def findRankForCitation(sorted_x, number):
    length = len(sorted_x)
    count = 0
    for item in sorted_x:
        count = count + 1
        if item[0] == number:
            #return length-count
            return (float(length)-float(count))/float(length)
    #return length
    return 1

def mainEnron():
    result = []
    for i in range(80):
        G=readNet('resultFullData.txt',927590400+1209600*i)
        #nx.draw(G)
        G = updateWeight(G, 927590400+1209600*i)
        x = nx.betweenness_centrality(G,weight = 'weight')
        #x = betweenness_centrality(G)
        #x = closeness_centrality(G)
        sorted_x = sorted(x.items(), key=operator.itemgetter(1))
        #tempResult = findRank(sorted_x,'louise.kitchen@enron.com')
        #tempResult = findRank(sorted_x,'lavorato@enron.com')
        #tempResult = findRank(sorted_x,'kenneth.lay@enron.com')
        tempResult = findRank(sorted_x,'jeff.skilling@enron.com')
        print str(i) + ': ' + str(tempResult)
        result.append(151-tempResult)
    
    plt.figure(0)
    plt.axis([0, 80, 0, 155])    
    plt.plot(result)
    plt.show()

def mainCitation():
    result = []
    for i in range(2,10):
        G=readNet('resultCitationData.txt',757382400+31622400*i)
        print "read data finish"
        #nx.draw(G)
        G = updateWeight(G, 757382400+31622400*i)
        print "update weight finish"
        x = nx.betweenness_centrality(G,weight = 'weight')
        #x = betweenness_centrality(G)
        #x = closeness_centrality(G)
        print "finish betweenness calculation"
        sorted_x = sorted(x.items(), key=operator.itemgetter(1))
        print "finish ranking"
        #tempResult = findRank(sorted_x,'louise.kitchen@enron.com')
        #tempResult = findRank(sorted_x,'lavorato@enron.com')
        #tempResult = findRank(sorted_x,'kenneth.lay@enron.com')
        #tempResult = findRank(sorted_x,'jeff.skilling@enron.com')
        tempResult = findRankForCitation(sorted_x,'9503124')
        print str(i) + ': ' + str(tempResult)
        #result.append(151-tempResult)
    
    plt.figure(0)
    #plt.axis([0, 80, 0, 155])    
    plt.plot(result)
    plt.show()
    
mainCitation()