#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 17:48:15 2017

@author: zhangchi
"""

# kEdge

class Solution(object):
    def __init__(self, probList):
        self.probList = probList
        self.count = 0

    def kEdge(self,i,j):
        if i == j:
            return [1-self.probList[i],self.probList[i]], self.count
        else:
            length = j - i + 1
            leftLength = length // 2
            if length % 2 == 1:
                rightLength = leftLength + 1
            else:
                rightLength = leftLength
            left, _ = self.kEdge(i, i + leftLength - 1)
            right, _ = self.kEdge(i + leftLength, j)
            result = (length + 1) * [0]
            for n in xrange(length + 1):
                for k in xrange(n + 1):
                    if k <= leftLength and (n-k) <= rightLength:
                        result[n] += left[k] * right[n-k]
                        self.count += 1
            return result, self.count

a = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.1]
s = Solution(a)
print s.kEdge(0,len(a)-1)
