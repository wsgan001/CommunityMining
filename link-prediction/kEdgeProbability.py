#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 21:23:25 2017

@author: zhangchi
"""

class Solution(object):
    def __init__(self, probList):
        self.probList = probList
        self.length = len(probList)
        self.dic = {}
        for i in xrange(1,self.length+1):
            self.dic[(i,1,1)] = probList[i-1]
            self.dic[(i,1,0)] = 1 - probList[i-1]
            
    def getResult(self):
        self.merge(1,self.length)
        return self.dic
    
    def merge(self,position,length):
        if length == 1:
            return
        else:
            leftLength = length // 2 # 左边的长度<=右边的长度
            rightLength = length - leftLength
            self.merge(position,leftLength)
            self.merge(position+leftLength,rightLength)
            for i in xrange(length+1):
                self.dic[(position,length,i)] = 0
                for j in xrange(leftLength+1):
                    if (position,leftLength,j) in self.dic and (position+leftLength,rightLength,i-j) in self.dic:
                        self.dic[(position,length,i)] += self.dic[(position,leftLength,j)] * self.dic[(position+leftLength,rightLength,i-j)]
                        
s = Solution([0.6,0.7,0.8])
dic = s.getResult()
print dic

# [0.6,0.7,0.8] 验算正确
# 0.6*0.7*0.2+0.6*0.3*0.8+0.4*0.7*0.8 = 0.452
# 0.6*0.3*0.2+0.4*0.7*0.2+0.4*0.3*0.8 = 0.188
# 0.6*0.7*0.8 = 0.336
# 0.3*0.4*0.2 = 0.024
                
        
# =============================================================================
# import numpy as np
# 
# # complexity from O^3 to O^4 (weight vs. probability)
# # calculate the summation of the possibilities of all subsets with exactly k edges in S
# 
# probList = [0.6, 0.7, 0.8, 0.9, 0.6, 0.7, 0.8, 0.9, 0.6, 0.7, 0.8, 0.9, 0.6, 0.7, 0.8, 0.9]
# length = len(probList)
# dic = {}
# for i in xrange(1,length+1):
#     dic[(i,1,1)] = probList[i-1]
#     dic[(i,1,0)] = 1 - probList[i-1]
# l = int(np.log2(length))
# count = 0
# for r in xrange(1,l+1):
#     t = 2 ** r
#     for i in xrange(1, length-t/2+1, t):
#         for k in xrange(0, t+1):
#             dic[(i,t,k)] = 0 # 最后的这个t有问题
#             for g in xrange(min(k,t/2)+1):
#                 if (i,t/2,g) in dic and (i+t/2,t/2,k-g) in dic:
#                     count += 1
#                     dic[(i,t,k)] += dic[(i,t/2,g)] * dic[(i+t/2,t/2,k-g)]
# print dic
# print count
# =============================================================================
  
# =============================================================================
# # 验算              
# probList = [0.7, 0.8]
# 0.5599999999999999*0.25+0.06*0.5+0.38*0.333333333 = 0.29666666653999996
# 1./12*0.7*0.8-1./6*1.5+0.5 = 0.29666666666666663
# =============================================================================


