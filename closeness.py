#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 13:04:45 2017

@author: zhangchi
"""

import networkx as nx
from ML_Handicapped_Paths import ML_Handicapped_Paths

def closeness_centrality(G, u=None, normalized=False):

    path_length = ML_Handicapped_Paths

    if u is None:
        nodes = G.nodes()
    else:
        nodes = [u]
    closeness_centrality = {}
    for n in nodes:
        G, S = path_length(G,n,0.3)
        sp = {o:G.node[o]['path_length'] for o in S}
        totsp = sum(sp.values())
        if totsp > 0.0 and len(G) > 1:
            #closeness_centrality[n] = (len(sp)-1.0) / totsp
            closeness_centrality[n] = 1 / totsp + ((len(G) - len(sp)) * 10)
            # normalize to number of nodes-1 in connected part
            if normalized:
                s = (len(sp)-1.0) / ( len(G) - 1 )
                closeness_centrality[n] *= s
        else:
            closeness_centrality[n] = 0.0
    if u is not None:
        return closeness_centrality[u]
    else:
        return closeness_centrality

def main():
    G = nx.Graph()
    '''
    G.add_edge('a','c',weight=0.8)
    G.add_edge('c','d',weight=0.8)
    G.add_edge('b','d',weight=0.8)
    G.add_edge('a','d',weight=0.8)
    G.add_edge('b','c',weight=0.8)
    G.add_edge('c','e',weight=0.8)
    G.add_edge('d','e',weight=0.8)
    G.add_edge('c','f',weight=0.8)
    G.add_edge('d','f',weight=0.8)
    G.add_edge('e','f',weight=0.8)
    G.add_edge('e','g',weight=0.8)
    G.add_edge('e','h',weight=0.8)
    G.add_edge('f','g',weight=0.8)
    G.add_edge('f','h',weight=0.8)
    G.add_edge('g','i',weight=0.8)
    G.add_edge('h','i',weight=0.8)
    G.add_edge('h','j',weight=0.8)
    G.add_edge('b','k',weight=0.8)
    G.add_edge('k','i',weight=0.8)
    '''
    G.add_edge('a','b',weight=0.8)
    G.add_edge('b','c',weight=0.8)
    G.add_edge('b','d',weight=0.8)
    G.add_edge('d','c',weight=0.8)
    G.add_edge('e','f',weight=0.8)
    G.add_edge('f','h',weight=0.8)
    G.add_edge('e','g',weight=0.8)
    G.add_edge('g','i',weight=0.8)
    G.add_edge('i','h',weight=0.8)

    print closeness_centrality(G,normalized=False)
    
main()