#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 00:51:53 2017

@author: zhangchi
"""

 
import networkx as nx
#import numpy as np
#import matplotlib.pyplot as plt 
#import random
import operator

# Routine for reading in a network as an edge list.
def readnet(input_file , sep_char=' ' , comment_char='#'): 
    num_lines = 0
    G = nx.Graph()
    for line in open(input_file):
        num_lines += 1
        if line[0] != comment_char:
            line = line.rstrip().split(sep_char) 
            if len(line) == 2:
                G.add_edge(int(line[0]), int(line[1])) 
                if num_lines < 10:
                    print line[0] + " " + line[1] 
                if num_lines == 10:
                    print "..."
    print 'Read ' + str(num_lines) + ' lines.'
    print 'Network has %d nodes and %d edges.' % (G.number_of_nodes(), G.number_of_edges())
    return G

G=readnet('enronData.txt')
nx.draw(G)
x = nx.degree_centrality(G)
sorted_x = sorted(x.items(), key=operator.itemgetter(1))
    