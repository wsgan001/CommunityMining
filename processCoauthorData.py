#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 11:54:09 2017

@author: zhangchi
"""

#inputFile = open('0326data.txt','r')
inputFile = open('dblp.xml','r')
result =[]
#allResult = []
count = 0
count_time = 0
author = []
date = None
for line in inputFile:
    line = line.strip()
    #allResult.append(line)
    if '<article mdate="' in line:
        date = line.split('<article mdate="')[1].split('"')[0]
        author = []
    elif '<author>' in line:
        authorTemp = line.split('<author>')[1].split('</author>')[0]
        author.append(authorTemp)
    elif '</article>' in line:
        if len(author) > 1:
            authorList = ''
            for item in author:
                authorList += item+'//// '
            print date + ": " + authorList
            count += 1

        