#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 21:23:25 2017

@author: zhangchi
"""

import numpy as np

# calculate the summation of the possibilities of all subsets with exactly k edges in S

probList = [0.7, 0.8]
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
  
# =============================================================================
# # 验算              
# probList = [0.7, 0.8]
# 0.5599999999999999*0.25+0.06*0.5+0.38*0.333333333 = 0.29666666653999996
# 1./12*0.7*0.8-1./6*1.5+0.5 = 0.29666666666666663
# =============================================================================


