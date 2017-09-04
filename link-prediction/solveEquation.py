#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 17:35:02 2017

@author: zhangchi
"""

import numpy as np
from kEdgeProbability import Solution

s = Solution()

#a = [] 
a_dic = s.getDic(a)
lengthA = len(a)
unknownNumber = lengthA - 1

b = [0.10071618034104506, 0.6234681082803037]
b_dic = s.getDic(b)
b2 = b_dic[(1,2,2)]
b1 = b_dic[(1,2,1)]
b0 = b_dic[(1,2,0)]

left = []
for i in xrange(unknownNumber):
    if i == 0:
        left.append([0]*(unknownNumber-1)+[b2])
    elif i == 1:
        left.append([0]*(unknownNumber-2)+[b2,b1])
    else:
        left.append([0]*(unknownNumber-i-1)+[b2,b1,b0]+[0]*(i-2))
right = []
for i in xrange(unknownNumber+1,1,-1):
    right.append(a_dic[(1,lengthA,i)])
left = np.array(left,dtype=np.float)
right = np.array(right,dtype=np.float)
x = np.linalg.solve(left, right)