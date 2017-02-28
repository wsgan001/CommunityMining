#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 01:06:16 2017

@author: zhangchi
"""

inputFile = open("FinalAdjacencyMatrix.csv")
x = 0
for line in inputFile:
    y = 0
    if x > 0:
        for item in line.split(','):
            if y > 0:
                if float(item) != 0:
                    print str(x)+ ' ' + str(y)
            y = y + 1
    x = x + 1