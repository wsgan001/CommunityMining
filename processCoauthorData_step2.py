#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 15:17:51 2017

@author: zhangchi
"""

inputFile = open('coauthorData_multiAuthor.txt','r')

dictionary = {}
for line in inputFile:
    line = line.strip().split(': ')
    date = line[0].split('-')
    dateNumber = int(date[0]+date[1]+date[2])
    if dateNumber in dictionary:
        dictionary[dateNumber].append(line[1])
    else:
        dictionary[dateNumber] = [line[1]]
    