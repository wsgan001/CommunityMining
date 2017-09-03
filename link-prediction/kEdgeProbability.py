#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 21:23:25 2017

@author: zhangchi
"""

from time import time

class Solution(object):            
    def getResult(self, probList):
        self.probList = probList
        self.length = len(probList)
        if self.length == 0:
            return 1
        self.dic = {}
        for i in xrange(1,self.length+1):
            self.dic[(i,1,1)] = probList[i-1]
            self.dic[(i,1,0)] = 1 - probList[i-1]
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
   
def test():                     
    s = Solution()
    
    a = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    lengthA = len(a)
    dic = s.getResult(a)
    dicFull = {}
    for i in xrange(lengthA+1):
        dicFull[(1,lengthA,i)] = dic[(1,lengthA,i)]
        
    for _ in xrange(276):
        b = [0.1, 0.2]
        lengthB = len(b)
        dic = s.getResult(b)
        dicShort = {}
        for i in xrange(lengthB+1):
            dicShort[(1,lengthB,i)] = dic[(1,lengthB,i)]
            
        del dic
        
        resultDic = {}
        length = lengthA - lengthB
        resultDic[(1,length,length+1)] = resultDic[(1,length,length+2)] = 0 # 避免后面if-else
        for i in xrange(length,-1,-1):
            resultDic[(1,length,i)] = (dicFull[(1,lengthA,i+2)] - \
            resultDic[(1,length,i+1)] * dicShort[(1,2,1)] - \
            resultDic[(1,length,i+2)] * dicShort[(1,2,0)]) / dicShort[(1,2,2)]
            
        resultDic.pop((1,length,length+1))
        resultDic.pop((1,length,length+2))
                
        print resultDic
        
def test2():                     
    s = Solution()
    
    for _ in xrange(276):
        a = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
        lengthA = len(a)
        dic = s.getResult(a)
        dicFull = {}
        for i in xrange(lengthA+1):
            dicFull[(1,lengthA,i)] = dic[(1,lengthA,i)]

t0 = time()
test()
t1 = time()
print t1 - t0

# =============================================================================
# class Solution(object):            
#     def getResult(self, probList):
#         self.probList = probList
#         self.length = len(probList)
#         if self.length == 0:
#             return 1
#         self.dic = {}
#         for i in xrange(1,self.length+1):
#             self.dic[(i,1,1)] = probList[i-1]
#             self.dic[(i,1,0)] = 1 - probList[i-1]
#         self.merge(1,self.length)
#         result = 0
#         for i in xrange(self.length+1):
#             result += 1/float(i+2) * self.dic[(1,self.length,i)]
#         return self.dic, result
#     
#     def merge(self,position,length):
#         if length == 1:
#             return
#         else:
#             leftLength = length // 2 # 左边的长度<=右边的长度
#             rightLength = length - leftLength
#             self.merge(position,leftLength)
#             self.merge(position+leftLength,rightLength)
#             for i in xrange(length+1):
#                 self.dic[(position,length,i)] = 0
#                 for j in xrange(leftLength+1):
#                     if (position,leftLength,j) in self.dic and (position+leftLength,rightLength,i-j) in self.dic:
#                         self.dic[(position,length,i)] += self.dic[(position,leftLength,j)] * self.dic[(position+leftLength,rightLength,i-j)]
#    
# def test():                     
#     s = Solution()
#     a = [0.5]
#     dic, result = s.getResult(a)
#     for i in xrange(len(a)+1):
#         print str((1,len(a),i)) + ":" + str(dic[(1,len(a),i)])
#     print result
#     
# test()
# =============================================================================

# =============================================================================
# [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
# (1, 8, 0):0.0036288
# (1, 8, 1):0.0373392
# (1, 8, 2):0.1460232
# (1, 8, 3):0.2832848
# (1, 8, 4):0.29724
# (1, 8, 5):0.1716432
# (1, 8, 6):0.0527048
# (1, 8, 7):0.0077328
# (1, 8, 8):0.0004032
# 
# (1, 6, 0):0.00504
# (1, 6, 1):0.05004
# (1, 6, 2):0.1846
# (1, 6, 3):0.3254
# (1, 6, 4):0.2902
# (1, 6, 5):0.12456
# (1, 6, 6):0.02016
# 
# (1, 2, 0):0.72
# (1, 2, 1):0.26
# (1, 2, 2):0.02
# 
# 0.02*0.02016 = 0.00040320000000000004
# (0.0077328-0.02016*0.26)/0.02 = 0.12455999999999995
# (0.0527048-0.02016*0.72-0.12456*0.26)/0.02 = 0.2902000000000002
# =============================================================================


# =============================================================================
# class Solution(object):
#     def __init__(self, probList):
#         self.probList = probList
#         self.length = len(probList)
#         self.dic = {}
#         for i in xrange(1,self.length+1):
#             self.dic[(i,1,1)] = probList[i-1]
#             self.dic[(i,1,0)] = 1 - probList[i-1]
#             
#     def getResult(self):
#         self.merge(1,self.length)
#         return self.dic
#     
#     def merge(self,position,length):
#         if length == 1:
#             return
#         else:
#             leftLength = length // 2 # 左边的长度<=右边的长度
#             rightLength = length - leftLength
#             self.merge(position,leftLength)
#             self.merge(position+leftLength,rightLength)
#             for i in xrange(length+1):
#                 self.dic[(position,length,i)] = 0
#                 for j in xrange(leftLength+1):
#                     if (position,leftLength,j) in self.dic and (position+leftLength,rightLength,i-j) in self.dic:
#                         self.dic[(position,length,i)] += self.dic[(position,leftLength,j)] * self.dic[(position+leftLength,rightLength,i-j)]
#                         
# s = Solution([0.6,0.7,0.8])
# dic = s.getResult()
# print dic
# =============================================================================

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


