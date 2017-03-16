#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 11:53:45 2017

@author: zhangchi
"""
import time
import datetime

inputFile = open('data.csv')
for line in inputFile:
    record = line.strip().split(',')
    recordTime = record[0].split('"')[1].split(' ')[0].split('-')
    d = datetime.date(int(recordTime[0]),int(recordTime[1]),int(recordTime[2]))
    unixtime = time.mktime(d.timetuple())
    print str(int(unixtime)) + ' ' + record[1] + ' ' + record[2]