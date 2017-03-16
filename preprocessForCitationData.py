#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 18:54:30 2017

@author: zhangchi
"""

import time
import datetime

inputFile = open('hep-th-citations.txt')
dictionary = {}
for line in inputFile:
    record = line.strip().split(' ')
    if int(record[0]) > int(record[1]):
        year = int(record[0][:2])
        if year > 90:
            year = year + 1900
        else:
            year = year + 2000
        month = int(record[0][2:4])
        #recordTime = record[0].split('"')[1].split(' ')[0].split('-')
        d = datetime.date(year,month,1)
        unixtime = time.mktime(d.timetuple())
        if unixtime in dictionary:
            dictionary[unixtime].append(record)
        else:
            dictionary[unixtime] = [record]

for unixtime in sorted(dictionary):
    for record in dictionary[unixtime]:
        print str(int(unixtime)) + ' ' + record[0] + ' ' + record[1]