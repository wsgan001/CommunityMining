#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 21:23:25 2017

@author: zhangchi
"""

import numpy as np

# calculate the summation of the possibilities of all subsets with exactly k edges in S

probList = [0.5, 0.6, 0.7, 0.8, 0.9, 0.5, 0.4, 0.2]
length = len(probList)
dic = {}
for i in xrange(1,length+1):
    dic[(i,1,1)] = probList[i-1]
    dic[(i,1,0)] = 1 - probList[i-1]
l = int(np.log2(length))
for r in xrange(1,l+1):
    t = 2 ** r
    for i in xrange(1, length-t/2+1, t):
        for k in xrange(0, t+1):
            dic[(i,t,k)] = 0
            for g in xrange(min(k,t/2)+1):
                if (i,t/2,g) in dic and (i+t/2,t/2,k-g) in dic:
                    dic[(i,t,k)] += dic[(i,t/2,g)] * dic[(i+t/2,t/2,k-g)]
print dic
                


