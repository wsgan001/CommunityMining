#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 22:48:58 2017

@author: zhangchi
"""

File = open("/Users/zhangchi/Desktop/cs690/CommunityMining/community-detection/dolphins/dolphins.gml")
for line in File:
    print line.split('\n')[0] + ' '